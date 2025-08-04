# K-Beauty Trend Briefing Frontend

A modern React frontend for the K-Beauty Trend Briefing System, built with Next.js, Tailwind CSS, and shadcn/ui.

## 🚀 Features

- **Dashboard**: View the latest daily K-beauty trend briefing with executive summary and trend analysis
- **Archive**: Browse all past briefings with search and filter functionality
- **Download**: Export briefings as Markdown or JSON files
- **Responsive Design**: Mobile-friendly interface with beautiful K-beauty branding
- **Real-time Updates**: Connect to the FastAPI backend for live data
- **Animations**: Smooth transitions and micro-interactions with Framer Motion

## 🛠️ Tech Stack

- **Framework**: Next.js 14 with App Router
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui
- **Animations**: Framer Motion
- **Icons**: Lucide React
- **TypeScript**: Full type safety
- **API**: Custom API client for FastAPI backend

## 📁 Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router pages
│   │   ├── page.tsx           # Dashboard (homepage)
│   │   ├── archive/
│   │   │   └── page.tsx       # Archive page
│   │   ├── subscribe/
│   │   │   └── page.tsx       # Subscribe page (placeholder)
│   │   └── globals.css        # Global styles
│   ├── components/
│   │   ├── ui/                # shadcn/ui components
│   │   ├── Navigation.tsx     # Main navigation layout
│   │   ├── TrendCard.tsx      # Individual trend display
│   │   └── BriefingListItem.tsx # Archive item component
│   └── lib/
│       ├── api.ts             # API client for backend
│       └── types.ts           # TypeScript interfaces
├── public/                    # Static assets
└── package.json
```

## 🎨 Design System

### Color Palette
- **Primary**: Pink (#ec4899) - K-beauty theme
- **Secondary**: Purple (#8b5cf6) - Complementary
- **Accent**: Blue (#3b82f6) - Information
- **Success**: Green (#10b981) - Positive actions
- **Warning**: Yellow (#f59e0b) - Medium impact
- **Error**: Red (#ef4444) - High impact

### Typography
- **Headings**: Inter (font-bold)
- **Body**: Inter (font-normal)
- **Code**: JetBrains Mono

### Components
- **Cards**: Rounded corners, subtle shadows, gradient backgrounds
- **Buttons**: Consistent styling with hover states
- **Badges**: Color-coded for different impact levels
- **Navigation**: Sidebar layout with mobile responsiveness

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ 
- npm or yarn
- FastAPI backend running on `localhost:8000`

### Installation

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Set up environment variables**:
   Create a `.env.local` file:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

3. **Start the development server**:
   ```bash
   npm run dev
   ```

4. **Open your browser**:
   Navigate to `http://localhost:3000`

## 📱 Pages

### Dashboard (`/`)
- Displays the latest daily briefing
- Shows executive summary, key insights, and trend analysis
- Download buttons for Markdown and JSON exports
- Real-time data from the FastAPI backend

### Archive (`/archive`)
- Lists all past briefings
- Search functionality to filter by keywords
- Modal view for detailed briefing information
- Responsive grid layout

### Subscribe (`/subscribe`)
- Placeholder for future subscription features
- Email digest, mobile app, and weekly report options
- Coming soon functionality

## 🔧 API Integration

The frontend connects to the FastAPI backend through a custom API client (`src/lib/api.ts`):

### Endpoints Used
- `GET /latest` - Get the latest briefing
- `GET /briefings` - Get all briefings
- `GET /briefings/{id}` - Get specific briefing
- `GET /download/markdown/{id}` - Download as Markdown
- `GET /download/json/{id}` - Download as JSON
- `GET /status` - Get pipeline status
- `POST /trigger` - Trigger new briefing

### Error Handling
- Graceful error states with retry functionality
- Loading states for better UX
- Network error detection and user feedback

## 🎯 Key Features

### Trend Cards
- Color-coded impact badges (High/Medium/Low)
- Category icons and labels
- Time-to-market indicators
- Keyword tags
- Hover animations

### Search & Filter
- Real-time search across briefing content
- Filter by date, keywords, or briefing ID
- Responsive search interface

### Download Functionality
- One-click download of briefings
- Multiple format support (Markdown, JSON)
- Progress indicators during download

### Responsive Design
- Mobile-first approach
- Sidebar navigation on desktop
- Mobile hamburger menu
- Touch-friendly interactions

## 🎨 Customization

### Styling
- Modify `src/app/globals.css` for global styles
- Update Tailwind config for custom colors/themes
- Custom animations in CSS

### Components
- All components are modular and reusable
- Easy to extend with new features
- TypeScript interfaces for type safety

### API Integration
- Centralized API client in `src/lib/api.ts`
- Easy to modify endpoints or add new ones
- Error handling and retry logic

## 🚀 Deployment

### Build for Production
```bash
npm run build
npm start
```

### Environment Variables
- `NEXT_PUBLIC_API_URL`: Backend API URL
- Set to your production API endpoint

### Static Export (Optional)
```bash
npm run export
```

## 🔧 Development

### Adding New Components
1. Create component in `src/components/`
2. Add TypeScript interfaces in `src/lib/types.ts`
3. Import and use in pages

### Adding New Pages
1. Create page in `src/app/`
2. Add to navigation in `src/components/Navigation.tsx`
3. Update routing as needed

### API Integration
1. Add new endpoints to `src/lib/api.ts`
2. Update TypeScript interfaces in `src/lib/types.ts`
3. Use in components with proper error handling

## 🐛 Troubleshooting

### Common Issues

**API Connection Errors**
- Ensure backend is running on `localhost:8000`
- Check CORS settings in FastAPI
- Verify environment variables

**Build Errors**
- Clear `.next` folder and rebuild
- Check TypeScript types
- Verify all dependencies installed

**Styling Issues**
- Check Tailwind CSS configuration
- Verify shadcn/ui components installed
- Clear browser cache

## 📄 License

This project is part of the K-Beauty Trend Briefing System.

## 🤝 Contributing

1. Follow the existing code structure
2. Use TypeScript for all new code
3. Add proper error handling
4. Test on mobile and desktop
5. Update documentation as needed
