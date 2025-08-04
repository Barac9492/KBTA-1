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
      console.log('Making API request to:', url);
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      });

      console.log('Response status:', response.status);
      if (!response.ok) {
        const errorText = await response.text();
        console.log('Response error:', errorText);
        throw new Error(`HTTP ${response.status}: ${errorText}`);
      }

      const data = await response.json();
      console.log('Response data:', data);
      return { success: true, data };
    } catch (error) {
      console.error(`API request failed for ${endpoint}:`, error);
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Unknown error' 
      };
    }
  }

  // Get latest briefing with timeout and enhanced error handling
  async getLatestBriefing(): Promise<ApiResponse<DailyBriefing>> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => {
      console.log('Request timeout - aborting');
      controller.abort();
    }, 60000); // 60 second timeout

    try {
      console.log('Making API request to /latest with timeout...');
      
      const url = `${this.baseUrl}/latest`;
      console.log('Request URL:', url);
      
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        signal: controller.signal,
      });

      clearTimeout(timeoutId);
      console.log('Response status:', response.status);
      
      if (!response.ok) {
        const errorText = await response.text();
        console.log('Response error:', errorText);
        throw new Error(`HTTP ${response.status}: ${errorText}`);
      }

      const data = await response.json();
      console.log('Raw API response:', data);
      
      // Handle the API response format - data is directly under response.data
      let briefingData: DailyBriefing;
      
      if (data.status === 'success' && data.data) {
        console.log('Using success status with nested data structure');
        briefingData = data.data;
      } else if (data.data) {
        console.log('Using nested data structure');
        briefingData = data.data;
      } else if (data.status === 'no_json_data') {
        console.log('No JSON data available');
        return { 
          success: false, 
          error: 'No briefing data available yet. Please run analysis first.' 
        };
      } else {
        // If no nested data, try to use the response.data directly
        console.log('Using direct data structure');
        briefingData = data as DailyBriefing;
      }

      // Fix enum mapping if needed
      if (briefingData.trend_analysis?.trends) {
        briefingData.trend_analysis.trends = briefingData.trend_analysis.trends.map(trend => ({
          ...trend,
          category: trend.category?.toUpperCase().replace(/_/g, '') as string || 'CONSUMERBEHAVIOR'
        }));
      }

      console.log('Processed briefing data:', briefingData);
      return { success: true, data: briefingData };
      
    } catch (error) {
      clearTimeout(timeoutId);
      console.error('API request failed:', error);
      
      if (error instanceof Error) {
        if (error.name === 'AbortError') {
          return { 
            success: false, 
            error: 'Request timeout - please refresh the page' 
          };
        }
        return { 
          success: false, 
          error: error.message || 'Unknown error' 
        };
      }
      
      return { 
        success: false, 
        error: 'Failed to load briefing data' 
      };
    }
  }

  // Get all briefings
  async getBriefings(): Promise<ApiResponse<BriefingListItem[]>> {
    const response = await this.request<{ data?: BriefingListItem[]; status?: string; error?: string }>('/briefings');
    
    if (response.success && response.data) {
      // Handle the nested API response format
      if (response.data.data) {
        return { success: true, data: response.data.data };
      } else if (response.data.status === 'no_data') {
        return { 
          success: true, 
          data: [] 
        };
      }
    }
    
    return { 
      success: false, 
      error: 'Failed to load briefings' 
    };
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
  async triggerBriefing(): Promise<ApiResponse<{ message: string }>> {
    return this.request<{ message: string }>('/trigger', {
      method: 'POST',
      body: JSON.stringify({ 
        force_refresh: false,
        include_notion_push: true,
        analysis_type: "full"
      }),
    });
  }

  // Download latest briefing as markdown
  async downloadMarkdown(): Promise<ApiResponse<Blob>> {
    try {
      const response = await fetch(`${this.baseUrl}/markdown`);
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP ${response.status}: ${errorText}`);
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

  // Download latest briefing as JSON
  async downloadJson(): Promise<ApiResponse<Blob>> {
    try {
      const response = await fetch(`${this.baseUrl}/download/json`);
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP ${response.status}: ${errorText}`);
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

  // Get API configuration
  async getConfig(): Promise<ApiResponse<{
    openai_configured: boolean;
    notion_configured: boolean;
    data_directory: string;
    agents_directory: string;
    output_directory: string;
    vercel_environment: boolean;
  }>> {
    return this.request<{
      openai_configured: boolean;
      notion_configured: boolean;
      data_directory: string;
      agents_directory: string;
      output_directory: string;
      vercel_environment: boolean;
    }>('/config');
  }
}

export const apiClient = new ApiClient(); 