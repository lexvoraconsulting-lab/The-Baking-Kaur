# Missing Assets for TBK Homepage

**Status:** BLOCKING — Hero image configuration incomplete

## Hero Image (Priority: CRITICAL)

**Official Specification Reference:** `HOMEPAGE_SPECIFICATION.md` §S1 (Editorial Hero v1.2)

**Current State:**
- Hero section configured for image (hero-image.liquid)
- No image currently selected in Shopify Admin
- Will render with placeholder text only until image is configured

**Requirement:**
Configure the hero image via Shopify Admin by selecting the image for product **b32** (Classic Strawberry Whipped Cream Cake).

### Source
**Product:** b32 — Classic Strawberry Whipped Cream Cake  
**Rationale:** This is the official TEMPORARY PRODUCTION HERO per the approved spec (see PROJECT_ROADMAP.md). Product b32 was selected because no other compliant designer-cake photography exists in the catalogue (all others carry watermarks, customer names, or third-party branding).

### Specifications
- **Product Handle:** b32
- **Image Source:** Shopify product image (first/featured image from product b32)
- **Desktop Dimensions:** 1196×1600px (portrait, 3:4 aspect ratio)
- **Format:** WebP with responsive srcset [600, 900, 1200, 1600px]
- **Loading:** Eager load + high fetchpriority (LCP optimization)
- **Alt Text:** "Classic Strawberry Whipped Cream Cake by The Baking Kaur"
- **Mobile Image:** Same image, mobile-optimized crop (optional separate image)

### Configuration Steps
1. Go to Shopify Admin → Themes → Current Theme → Theme Editor
2. Click "Homepage" (index)
3. Click "Hero" section
4. In section settings, select image from:
   - **Option A (Recommended):** Pick product b32 image directly
   - **Option B:** Upload custom image (dimensions: 1196×1600+, landscape or portrait acceptable)
5. Save

### Text Overlay (Already Configured)
- Heading: "Designer Cakes & Celebration Hampers"
- Subheading: "in Meerut"
- CTA 1: "SHOP CAKES" → /collections/cakes
- CTA 2: "SEND A SURPRISE" → /collections/hampers

### Visual Treatment
The image will display with:
- Responsive srcset for desktop/tablet/mobile
- Focal point handling (center default, adjustable)
- Text overlay with heading, subheading, CTAs
- No text overlay opacity/gradient (relying on text color contrast only)

---

## Future Photography (Backlog)

Per PROJECT_ROADMAP.md and COMPONENT_LIBRARY.md:

**Flagship Hero Photoshoot** — Planned upgrade from b32 product image to a dedicated premium hero lifestyle shot. Timeline: TBD.

Requirements for final hero:
- Premium designer/occasion cake (no customer names, no watermarks, no third-party branding)
- Warm ivory/cream/blush background OR natural studio setting
- Professional lighting (editorial quality)
- Lifestyle composition (cake + flowers + celebration elements optional)
- High resolution (3000px+ wide recommended)
- Source: TBK studio shoot or commissioned professional photography

---

## Deployment Impact

**Current Status:** Homepage will display with placeholder text only.  
**Critical Path:** Requires image selection in Shopify Admin before launch.  
**Fix Effort:** ~2 minutes (select image in theme editor).  
**Blocker:** YES — hero must have an image to match approved visual design.

---

**Last Updated:** 2026-08-13  
**Assigned To:** TBK Shopify Admin / Store Manager  
**Action Required:** Select product b32 image in Shopify Theme Editor  
**Timeline:** Before final homepage publication (QA/preview testing can continue with placeholder)
