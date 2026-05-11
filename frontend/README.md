# AI Website Builder - Frontend

React + TypeScript frontend for the AI-powered website builder platform.

## Tech Stack

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Ant Design 5** - UI component library
- **Tailwind CSS** - Utility-first CSS
- **GrapesJS** - Visual page editor
- **Zustand** - State management
- **React Router v6** - Routing
- **Axios** - HTTP client
- **React Markdown** - Markdown rendering

## Project Structure

```
frontend/src/
├── api/                      # API client and endpoint modules
│   ├── client.ts            # Axios instance with auth interceptor
│   ├── auth.ts              # Authentication APIs
│   ├── sites.ts             # Site management APIs
│   ├── pages.ts             # Page CRUD APIs
│   ├── ai.ts                # AI Builder APIs
│   ├── blog.ts              # Blog management APIs
│   ├── forms.ts             # Form submission APIs
│   ├── settings.ts          # Site settings APIs
│   ├── analytics.ts         # Analytics APIs
│   ├── assets.ts            # Asset upload APIs
│   ├── team.ts              # Team management APIs
│   ├── publish.ts           # Publishing APIs
│   └── templates.ts         # Template APIs
├── components/              # Reusable components
│   ├── Layout/
│   │   ├── AppLayout.tsx   # Main app layout
│   │   ├── Sidebar.tsx     # Navigation sidebar
│   │   └── Header.tsx      # Top header with user menu
│   ├── AIChat/
│   │   ├── ChatWindow.tsx  # AI chat conversation display
│   │   ├── ChatMessage.tsx # Individual chat message
│   │   └── ChatInput.tsx   # Chat input with file upload
│   ├── Editor/
│   │   └── GrapesEditor.tsx # GrapesJS wrapper component
│   └── common/
│       ├── Loading.tsx      # Loading spinner
│       └── ProtectedRoute.tsx # Auth guard for routes
├── pages/                   # Page components
│   ├── auth/
│   │   ├── Login.tsx       # Login page
│   │   └── Register.tsx    # Registration page
│   ├── dashboard/
│   │   └── Dashboard.tsx   # Main dashboard with site cards
│   ├── ai-builder/
│   │   └── AIBuilder.tsx   # AI chat builder interface
│   ├── editor/
│   │   └── Editor.tsx      # GrapesJS page editor
│   ├── admin/
│   │   ├── SiteSettings.tsx      # Site configuration
│   │   ├── BlogManager.tsx       # Blog post management
│   │   ├── FormSubmissions.tsx   # Form submission viewer
│   │   ├── Analytics.tsx         # Analytics dashboard
│   │   └── TeamManager.tsx       # Team member management
│   └── publish/
│       └── PublishPage.tsx # Publishing and domain management
├── store/                   # Zustand state stores
│   ├── authStore.ts        # Authentication state
│   ├── siteStore.ts        # Site and page state
│   └── editorStore.ts      # Editor state
├── types/                   # TypeScript type definitions
│   └── index.ts            # All type definitions
├── App.tsx                  # Main app component with routing
└── main.tsx                # App entry point
```

## Key Features Implemented

### 1. Authentication System
- Login page with email/password
- Registration with company name
- JWT token management with auto-refresh
- Protected routes with auth guard
- Persistent session via localStorage

### 2. Dashboard
- Site cards with status badges
- Quick stats (total sites, published, AI quota)
- Create new site modal with AI/Blank options
- Site preview and settings access

### 3. AI Builder (Core Feature)
- Split-screen interface: chat on left, preview on right
- Real-time chat with AI assistant
- Document upload support (PDF, Word, TXT)
- Streaming AI responses
- Live HTML preview of generated sites
- Generate/Regenerate functionality
- Direct transition to editor

### 4. Page Editor
- Full GrapesJS integration
- Custom blocks library:
  - Hero Banner
  - Features Grid
  - Contact Form
  - And more...
- Page selector dropdown
- Auto-save with debounce (2s)
- Responsive device preview
- Style manager and layer manager
- Block library and traits panel

### 5. Admin Pages

**Site Settings:**
- Company information
- Logo and favicon upload
- SEO settings
- Google Analytics integration
- Custom head/body code injection

**Blog Manager:**
- Create/edit/delete blog posts
- Status management (draft/published)
- Markdown content editor

**Form Submissions:**
- View all form submissions
- Status workflow (new/read/replied/archived)
- Export to CSV
- Detailed submission drawer

**Analytics:**
- Page view and visitor stats
- Top pages table
- Form submission counts
- Traffic trends (mock data for now)

**Team Manager:**
- Invite team members by email
- Role management (owner/editor/viewer)
- Remove members
- Last login tracking

### 6. Publishing
- One-click publish button
- Custom domain binding
- DNS configuration wizard with CNAME instructions
- SSL provisioning status tracker
- Version history table
- Rollback functionality

## API Integration

All API calls go through a centralized client (`src/api/client.ts`) with:
- Automatic JWT token attachment
- Token refresh on 401 errors
- Auto-redirect to login on auth failure
- Typed request/response interfaces

## State Management

Three main Zustand stores:

1. **authStore** - User authentication, tenant info, login/logout
2. **siteStore** - Sites and pages CRUD operations
3. **editorStore** - Editor instance, current page, dirty state

## Custom Blocks

The editor includes pre-built blocks for common website sections:
- Hero Banner with gradient background
- Features Grid (3-column)
- Contact Form with Tailwind styling
- More can be easily added in `Editor.tsx`

## Environment Variables

Create a `.env` file:

```bash
VITE_API_URL=http://localhost:8000/api/v1
VITE_ENV=development
```

## Development

```bash
# Install dependencies
npm install

# Start dev server (http://localhost:3000)
npm run dev

# Type check
npm run type-check

# Lint
npm run lint

# Build for production
npm run build

# Preview production build
npm run preview
```

## Build Output

The production build creates optimized bundles in `dist/`:
- `dist/index.html` - Entry HTML
- `dist/assets/` - JS/CSS bundles with hash names
- Gzip size: ~720KB (can be optimized with code splitting)

## Routing Structure

```
/login                          → Login page (public)
/register                       → Register page (public)
/                               → Dashboard (protected)
/ai-builder                     → AI Builder (protected, full-screen)
/sites/:siteId/editor           → Page Editor (protected, full-screen)
/sites/:siteId/settings         → Site Settings (protected)
/sites/:siteId/blog             → Blog Manager (protected)
/sites/:siteId/forms            → Form Submissions (protected)
/sites/:siteId/analytics        → Analytics (protected)
/sites/:siteId/publish          → Publish Page (protected)
/team                           → Team Manager (protected)
```

## Integration with Backend

The frontend expects the backend API at `http://localhost:8000/api/v1` (dev) with these endpoints:

- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `GET /auth/me` - Get current user
- `GET /sites` - List sites
- `POST /sites` - Create site
- `GET /sites/:id/pages` - List pages
- `POST /ai/sessions` - Create AI session
- `POST /ai/sessions/:id/message` - Send chat message
- `POST /sites/:id/publish` - Publish site
- And many more...

See `src/api/` for complete endpoint definitions.

## Next Steps

1. **Connect to real backend** - Currently mock data in some places
2. **Implement SSE streaming** - For real-time AI responses
3. **Add more GrapesJS blocks** - Expand the component library
4. **Code splitting** - Reduce initial bundle size
5. **Error boundaries** - Better error handling UI
6. **Loading states** - More granular loading indicators
7. **Form validation** - Enhanced client-side validation
8. **Image optimization** - Lazy loading and WebP support
9. **PWA features** - Service worker for offline support
10. **E2E tests** - Cypress or Playwright tests

## Known Issues

- GrapesJS plugins may need additional configuration for production
- Bundle size is large (~2.4MB), needs code splitting optimization
- Some TypeScript types could be more specific
- Missing comprehensive error handling in some components

## Contributing

When adding new features:

1. Add types to `src/types/index.ts`
2. Create API client methods in `src/api/`
3. Build UI components in `src/pages/` or `src/components/`
4. Update routing in `src/App.tsx`
5. Test the build with `npm run build`

## License

This project is part of the AI Website Builder SaaS platform.
