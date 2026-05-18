---
name: Vibrant Culinary Explorer
colors:
  surface: '#fbf9f8'
  surface-dim: '#dbdad9'
  surface-bright: '#fbf9f8'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f5f3f3'
  surface-container: '#efeded'
  surface-container-high: '#e9e8e7'
  surface-container-highest: '#e4e2e2'
  on-surface: '#1b1c1c'
  on-surface-variant: '#5b403f'
  inverse-surface: '#303031'
  inverse-on-surface: '#f2f0f0'
  outline: '#8f6f6e'
  outline-variant: '#e4bebc'
  surface-tint: '#bb162c'
  primary: '#b7122a'
  on-primary: '#ffffff'
  primary-container: '#db313f'
  on-primary-container: '#fffbff'
  inverse-primary: '#ffb3b1'
  secondary: '#5f5e5e'
  on-secondary: '#ffffff'
  secondary-container: '#e4e2e1'
  on-secondary-container: '#656464'
  tertiary: '#5b5c5c'
  on-tertiary: '#ffffff'
  tertiary-container: '#737575'
  on-tertiary-container: '#fcfcfc'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdad8'
  primary-fixed-dim: '#ffb3b1'
  on-primary-fixed: '#410007'
  on-primary-fixed-variant: '#92001c'
  secondary-fixed: '#e4e2e1'
  secondary-fixed-dim: '#c8c6c6'
  on-secondary-fixed: '#1b1c1c'
  on-secondary-fixed-variant: '#474747'
  tertiary-fixed: '#e2e2e2'
  tertiary-fixed-dim: '#c6c6c7'
  on-tertiary-fixed: '#1a1c1c'
  on-tertiary-fixed-variant: '#454747'
  background: '#fbf9f8'
  on-background: '#1b1c1c'
  surface-variant: '#e4e2e2'
typography:
  display-lg:
    fontFamily: metropolis
    fontSize: 40px
    fontWeight: '800'
    lineHeight: 48px
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: metropolis
    fontSize: 32px
    fontWeight: '800'
    lineHeight: 38px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: metropolis
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
  headline-md:
    fontFamily: metropolis
    fontSize: 20px
    fontWeight: '700'
    lineHeight: 28px
  body-lg:
    fontFamily: metropolis
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: metropolis
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-lg:
    fontFamily: metropolis
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: metropolis
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 14px
    letterSpacing: 0.02em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 4px
  xs: 8px
  sm: 12px
  md: 16px
  lg: 24px
  xl: 32px
  margin-mobile: 16px
  margin-desktop: 48px
  gutter: 16px
---

## Brand & Style

The design system is built to evoke hunger, excitement, and trust. It targets urban foodies and casual diners who seek immediate, high-quality visual information. The personality is **energetic, hospitable, and premium**.

The visual style is **Modern / High-Contrast**, leaning heavily into "appetizing" aesthetics. This is achieved through expansive white space that allows high-resolution food photography to pop, paired with a singular, high-energy brand color. The interface feels "juicy" through the use of soft, organic shapes and generous interactive targets, ensuring a mobile-first experience that feels effortless and inviting.

## Colors

The palette is dominated by **Crave Red (#E23744)**, a color scientifically associated with appetite stimulation and urgency. 

- **Primary:** Crave Red is used for primary actions, status indicators, and brand touchpoints.
- **Surface:** A "Clean Plate" white (#FFFFFF) is the base, with "Mist" (#F8F8F8) used for secondary containers and background grouping to prevent visual fatigue.
- **Typography:** "Charcoal" (#2D2D2D) provides high-contrast legibility for headings, while "Slate" (#696969) is reserved for secondary metadata and captions.
- **Accents:** Success states use a vibrant green (#48BB78) to signify "Open Now" or "Confirmed," while stars/ratings utilize a warm amber (#F6AD55).

## Typography

This design system utilizes **Metropolis**, a modern geometric sans-serif that balances mathematical precision with approachable, rounded terminals. 

Headlines use **Bold or Extra Bold** weights to create a strong hierarchy against busy food photography. Body text is set with generous line heights to ensure readability while scanning restaurant descriptions. For mobile, display sizes scale down aggressively to prevent awkward word breaks in tight grid layouts, maintaining a "tight" editorial feel.

## Layout & Spacing

The layout follows a **Fluid Grid** model with a heavy emphasis on vertical scrolling and horizontal "shelves" (carousels) for category discovery.

- **Mobile:** A 4-column layout with 16px side margins and 16px gutters.
- **Desktop:** A 12-column centered grid (max-width 1200px) with 24px gutters.
- **Rhythm:** An 8px linear scale is used for most spacing, but 12px (sm) is the "magic number" for internal component padding to maintain that "generous" and "approachable" feel requested.

Components should utilize "Safe Areas" around images to ensure text overlays are always legible, typically using a 15% black-to-transparent gradient wash at the bottom of food photos.

## Elevation & Depth

Depth is handled through **Ambient Shadows** and tonal layering rather than harsh borders.

- **Level 0 (Base):** White (#FFFFFF) or Mist (#F8F8F8) background.
- **Level 1 (Cards):** Subtle shadow (0px 4px 12px rgba(0,0,0,0.05)) with a 1px soft gray border (#E8E8E8) to define edges on white backgrounds.
- **Level 2 (Floating/Interactive):** Medium shadow (0px 8px 24px rgba(0,0,0,0.12)) used for "Order Now" bars or sticky navigation elements.
- **Level 3 (Modals):** High-diffusion shadow (0px 12px 40px rgba(0,0,0,0.18)) with a backdrop blur (8px) on the obscured content to keep the user focused on the selection.

## Shapes

The shape language is **Rounded and Organic**. 

- Standard components (Buttons, Input Fields) use a **12px (rounded-lg)** radius.
- Large containers (Restaurant Cards, Modals) use a **16px (rounded-xl)** radius to feel soft and premium.
- Search bars and filter chips utilize a **Pill-shape** to distinguish them from actionable primary buttons.
- Images should always inherit the corner radius of their parent container to maintain a unified, "friendly" silhouette.

## Components

### Buttons
- **Primary:** Solid Crave Red with white text. 12px corner radius. High-tap targets (min 48px height).
- **Secondary:** White background with a 1px border of Mist (#E8E8E8) and Charcoal text.

### Input Fields
- Floating labels with a 12px radius. On focus, the border shifts from Light Gray to Crave Red.
- Search bars include a left-aligned magnifying glass and a right-aligned "Filter" icon for high utility.

### Cards (Restaurant)
- Image-heavy. The top 60% is a 16:9 photo. The bottom 40% contains the name (Bold), rating (Badge style), and metadata (Price/Cuisine) with generous 16px internal padding.

### Chips
- Used for cuisines and filters. Pill-shaped, light gray background, transitions to Crave Red with white text when "Selected."

### Lists
- Clean separators using 1px Mist (#F8F8F8) lines. 16px vertical padding between items to ensure high scannability on mobile devices.

### Rating Badges
- Small, rounded rectangles (4px radius) with a green background for high ratings (>4.0) and gold for trending spots.