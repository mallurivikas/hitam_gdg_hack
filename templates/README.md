# Health AI - Pure HTML/CSS/JS Version

This is a pure HTML, CSS, and vanilla JavaScript version of the Health AI application. No frameworks, no build tools required - just open and run!

## 📁 Project Structure

```
pure-html/
├── index.html              # Home page
├── about.html             # About page
├── assessment.html        # Full health assessment form
├── quick-check.html       # Quick 2-minute health check
├── nutrition-scanner.html # Nutrition label scanner
├── demo.html              # Demo with sample results
├── css/
│   └── styles.css         # All styles (converted from Tailwind)
├── js/
│   ├── common.js          # Utility functions, icons, helpers
│   └── components.js      # Component loader for header/footer
└── components/
    ├── header.html        # Reusable header
    └── footer.html        # Reusable footer
```

## 🚀 How to Run

### Option 1: Simple File Open (Recommended for Development)
1. Open `index.html` in your web browser
2. Navigate between pages using the menu

**Note:** Due to CORS restrictions, the component loader (header/footer) may not work when opening files directly. Use Option 2 or 3 for full functionality.

### Option 2: Using Python HTTP Server
```bash
# Navigate to the pure-html directory
cd pure-html

# Python 3
python -m http.server 8000

# Python 2
python -m SimpleHTTPServer 8000

# Then open http://localhost:8000 in your browser
```

### Option 3: Using Node.js HTTP Server
```bash
# Install http-server globally (one time)
npm install -g http-server

# Navigate to the pure-html directory
cd pure-html

# Start the server
http-server -p 8000

# Then open http://localhost:8000 in your browser
```

### Option 4: Using VS Code Live Server Extension
1. Install "Live Server" extension in VS Code
2. Right-click on `index.html`
3. Select "Open with Live Server"

### Option 5: Using PHP Built-in Server
```bash
cd pure-html
php -S localhost:8000
```

## 📄 Pages

- **Home (`index.html`)** - Landing page with hero section, features, and stats
- **About (`about.html`)** - Information about the AI system and methodology
- **Full Assessment (`assessment.html`)** - Comprehensive health assessment form
- **Quick Check (`quick-check.html`)** - Fast 2-minute health check
- **Nutrition Scanner (`nutrition-scanner.html`)** - Upload food labels for analysis
- **Demo (`demo.html`)** - Sample patient profile with results

## ✨ Features

- ✅ **Pure HTML/CSS/JS** - No frameworks or dependencies
- ✅ **Responsive Design** - Works on desktop, tablet, and mobile
- ✅ **Reusable Components** - Header and footer loaded dynamically
- ✅ **Modern UI** - Clean, professional design with gradients and shadows
- ✅ **Interactive Forms** - Form validation and dynamic inputs
- ✅ **Toast Notifications** - User feedback system
- ✅ **Icon System** - SVG icons inline (no icon fonts needed)

## 🎨 Styling

All styles are in `css/styles.css`:
- CSS Variables for theming
- Responsive grid system
- Utility classes
- Component styles
- Mobile-first approach

## 🔧 JavaScript Utilities

### `common.js` Features:
- Toast notification system
- Navigation highlighting
- Mobile menu toggle
- BMI calculator
- Form validation
- Slider value updaters
- SVG icon library

### `components.js` Features:
- Dynamic header/footer loading
- Event listener management

## 🌐 Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Opera (latest)

## 📝 Customization

### Change Colors
Edit CSS variables in `css/styles.css`:
```css
:root {
  --primary: #0ea5e9;
  --accent: #f59e0b;
  --danger: #ef4444;
  /* ... */
}
```

### Add New Pages
1. Create new HTML file
2. Include header placeholder: `<div id="header-placeholder"></div>`
3. Include footer placeholder: `<div id="footer-placeholder"></div>`
4. Link CSS and JS files
5. Add navigation link in `components/header.html`

## 📦 No Build Process Required

Unlike the React version, this doesn't require:
- ❌ Node modules installation
- ❌ Build/compilation step
- ❌ Package managers
- ❌ Bundlers or transpilers

Just pure web technologies! 🎉

## 🔄 Converting from React

This version was converted from React + Tailwind CSS + TypeScript:
- React components → Pure HTML
- Tailwind classes → Custom CSS
- React hooks → Vanilla JavaScript
- React Router → Standard links
- Component props → HTML attributes

## 📱 Mobile Responsive

All pages are fully responsive with:
- Flexible grid layouts
- Mobile navigation menu
- Touch-friendly buttons
- Adaptive typography
- Optimized for all screen sizes

## 🚧 Development Tips

1. **Live Reload**: Use a development server with live reload for better experience
2. **Browser DevTools**: Use Console to debug JavaScript
3. **CSS Changes**: Refresh page to see CSS updates
4. **Component Updates**: Header/footer changes reflect immediately on all pages

## 📄 License

Same as the original React application.

## 🤝 Contributing

This is a static conversion of the original React app. For features that require backend API, you'll need to implement server-side logic separately.

---

**Enjoy your framework-free experience!** 🎊
