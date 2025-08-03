import { 
  DailyBriefing, 
  BriefingListItem, 
  PipelineStatus, 
  ApiResponse 
} from './types';

// Use relative path for API calls in production, fallback to localhost for development
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 
  (typeof window !== 'undefined' ? '/api' : 'http://localhost:8000');

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string, 
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    try {
      const url = `${this.baseUrl}${endpoint}`;
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return { success: true, data };
    } catch (error) {
      console.error(`API request failed for ${endpoint}:`, error);
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Unknown error' 
      };
    }
  }

  // Get latest briefing
  async getLatestBriefing(): Promise<ApiResponse<DailyBriefing>> {
    return this.request<DailyBriefing>('/latest');
  }

  // Get all briefings
  async getBriefings(): Promise<ApiResponse<BriefingListItem[]>> {
    return this.request<BriefingListItem[]>('/briefings');
  }

  // Get specific briefing by ID
  async getBriefing(id: string): Promise<ApiResponse<DailyBriefing>> {
    return this.request<DailyBriefing>(`/briefings/${id}`);
  }

  // Get pipeline status
  async getStatus(): Promise<ApiResponse<PipelineStatus>> {
    return this.request<PipelineStatus>('/status');
  }

  // Trigger new briefing
  async triggerBriefing(dryRun: boolean = false): Promise<ApiResponse<any>> {
    return this.request('/trigger', {
      method: 'POST',
      body: JSON.stringify({ dry_run: dryRun }),
    });
  }

  // Download briefing as markdown
  async downloadMarkdown(id: string): Promise<ApiResponse<Blob>> {
    try {
      const response = await fetch(`${this.baseUrl}/download/markdown/${id}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const blob = await response.blob();
      return { success: true, data: blob };
    } catch (error) {
      console.error('Download failed:', error);
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Download failed' 
      };
    }
  }

  // Download briefing as JSON
  async downloadJson(id: string): Promise<ApiResponse<Blob>> {
    try {
      const response = await fetch(`${this.baseUrl}/download/json/${id}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const blob = await response.blob();
      return { success: true, data: blob };
    } catch (error) {
      console.error('Download failed:', error);
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Download failed' 
      };
    }
  }

  // Health check
  async healthCheck(): Promise<ApiResponse<{ status: string }>> {
    return this.request<{ status: string }>('/health');
  }
}

export const apiClient = new ApiClient(); 