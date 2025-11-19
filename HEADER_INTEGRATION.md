# Header Integration Guide / دليل دمج Header

## 📁 File Structure / هيكل الملفات

```
frontend/src/
├── components/
│   └── header/
│       ├── Header.jsx          # Main header component
│       ├── NavLinks.jsx        # Desktop navigation links
│       ├── LanguageSwitcher.jsx # Language toggle (AR/EN)
│       ├── ThemeToggle.jsx     # Theme toggle (Light/Dark)
│       └── MobileMenu.jsx      # Mobile menu drawer
├── store/
│   └── themeStore.js           # Zustand store for theme & language
└── pages/
    └── ...
```

## ✅ Integration Complete / التكامل مكتمل

The Header has been integrated into `Layout.jsx`. It will automatically appear on all pages.

تم دمج Header في `Layout.jsx`. سيظهر تلقائياً على جميع الصفحات.

## 🎨 Features / الميزات

### 1. **Responsive Design**
- Desktop: Full navigation menu
- Tablet: Collapsed menu
- Mobile: Hamburger menu with full-screen drawer

### 2. **Language Toggle (AR/EN)**
- Switches between Arabic and English
- Automatically changes RTL ↔ LTR
- Saves preference in localStorage

### 3. **Theme Toggle (Light/Dark)**
- Switches between light and dark mode
- Uses Tailwind's `dark:` classes
- Saves preference in localStorage

### 4. **Animations**
- Smooth scroll detection
- Glassmorphism background on scroll
- Fade/slide animations for menu items
- Hover effects with scale and color transitions

### 5. **Navigation Items**
- AI Plant Analysis → `/upload`
- Smart Water Optimization → `/upload`
- Soil Health Detection → `/upload`
- Fertilizer & Pest Diagnosis → `/upload`
- SmartFarm Dashboard → `/dashboard`

## 🔧 Customization / التخصيص

### Change Navigation Items

Edit `NavLinks.jsx` and `MobileMenu.jsx`:

```javascript
const navItems = [
  {
    path: '/your-path',
    label: 'Your Label',
    labelAr: 'التسمية بالعربية',
    icon: YourIcon,
    gradient: 'from-color-500 to-color-500'
  }
]
```

### Change Colors

Edit `tailwind.config.js` to customize the color scheme.

### Adjust Animations

Edit animation values in Header components using Framer Motion props.

## 📝 Notes / ملاحظات

- Header is fixed at the top
- Automatically adjusts on scroll (blur effect)
- Mobile menu closes on route change
- Theme and language preferences persist across sessions

## 🚀 Ready to Use / جاهز للاستخدام

The Header is now fully integrated and ready to use! Just refresh your browser to see it.

Header الآن مدمج بالكامل وجاهز للاستخدام! فقط قم بتحديث المتصفح لرؤيته.

