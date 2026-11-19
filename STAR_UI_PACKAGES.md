# Star Ecosystem: 350+ Official UI Packages

**Version**: 1.0.0 (GA)  
**Standard**: Official Star UI Package Registry  
**Total UI Packages**: 351 Packages  
**Status**: Canonical Standard & Production Specification

---

## 1. Overview

The Star Language Package Registry contains **350+ modular UI packages** covering all aspects of modern web, mobile, and desktop application development. All packages are pure Star (`.star`) components, fully reactive, platform-independent, and installable via the official CLI:

```bash
# Search for UI packages
star search picker
star search chart
star search table

# Install a package into your project
star install ui/date_picker
star install ui/chart_line
star install ui/data_table
```

---

## 2. Catalog Breakdown by Domain

### 1. Forms, Inputs & Pickers (55 Packages)
| Package | Description |
| :--- | :--- |
| `ui/date_picker` | Calendar date selection dialog and input field |
| `ui/time_picker` | Clock face and 24h/12h time selector widget |
| `ui/date_range_picker` | Dual calendar date span and range selector |
| `ui/color_picker` | Hex, RGB, HSL and gradient interactive color picker |
| `ui/color_palette_wheel` | Circular color spectrum wheel and hue slider |
| `ui/rich_text_editor` | WYSIWYG formatted text editor with bold, italic, lists |
| `ui/markdown_editor` | Split-pane markdown source editor with live preview |
| `ui/code_editor` | Syntax-highlighted code editor with line numbering |
| `ui/slider_range` | Dual-thumb min/max range slider component |
| `ui/slider_stepped` | Discrete stepped numeric slider with tick marks |
| `ui/tag_input` | Chip-based tag entry with auto-suggestion and chip removal |
| `ui/file_uploader` | Drag-and-drop multi-file upload zone with progress bars |
| `ui/file_drop_zone` | Dashed border drag-and-drop file receiver with MIME filter |
| `ui/signature_pad` | Touch and mouse digital signature capture canvas |
| `ui/otp_input` | Auto-advancing segmented 4-to-6 digit OTP/PIN input |
| `ui/pin_code_field` | Secure masked PIN entry field with biometric icon |
| `ui/rating_bar` | Interactive 5-star or custom icon rating selector |
| `ui/autocomplete` | Typeahead autocomplete suggestions dropdown |
| `ui/masked_input` | Formatted input mask for phone numbers, SSN, and cards |
| `ui/phone_input` | International telephone number input with country flag |
| `ui/currency_input` | Real-time formatted monetary amount input with currency symbol |
| `ui/credit_card_input` | Smart card number formatter with auto card brand detection |
| `ui/checkbox_group` | Grouped tri-state checkbox list with select-all |
| `ui/radio_group` | Grouped single-selection radio button list with custom styling |
| `ui/switch_toggle` | Animated iOS and Material style toggle switch |
| `ui/stepper_input` | Incremental numeric +/- stepper with min/max bounds |
| `ui/cascader` | Hierarchical multi-level cascaded dropdown selector |
| `ui/transfer_list` | Dual-column shuttle box transfer list with move buttons |
| `ui/tree_select` | Hierarchical tree-view dropdown selector with search |
| `ui/mentions_input` | @mention and #hashtag suggestion popover input |
| `ui/password_strength` | Dynamic password security meter with rule checkmarks |
| `ui/search_bar` | Full-featured search bar with voice input icon and clear button |
| `ui/filter_panel` | Collapsible multi-criteria filter builder panel |
| `ui/multi_select` | Searchable multi-selection dropdown with chip tags |
| `ui/dropdown_select` | Standard customizable dropdown picker with icons |
| `ui/combo_box` | Hybrid text input and dropdown select combo box |
| `ui/segmented_picker` | iOS-style pill segmented control with sliding indicator |
| `ui/wheel_picker` | Scrollable 3D drum wheel picker for dates and lists |
| `ui/time_duration_picker` | Hours, minutes, seconds duration timer picker |
| `ui/quantity_selector` | E-commerce shopping cart item quantity adjuster |
| `ui/search_filter_chips` | Horizontal scrollable filter chips with active toggles |
| `ui/boolean_toggle_card` | Visual card with integrated switch and description |
| `ui/inline_edit_field` | Click-to-edit inline text field with save/cancel icons |
| `ui/expandable_search` | Collapsed search icon expanding into full search bar |
| `ui/geo_location_input` | Address autocomplete and GPS location capture field |
| `ui/dimension_input` | Width, height, depth 3D dimension input with unit toggle |
| `ui/ip_address_input` | Segmented IPv4 and IPv6 network address field |
| `ui/url_input` | Validated web URL input with protocol prefix pill |
| `ui/json_input_validator` | Live JSON syntax highlighting and validation editor |
| `ui/regex_tester_input` | Pattern tester input with live match highlighting |
| `ui/unit_converter_input` | Dual-field imperial to metric live converter input |
| `ui/percentage_slider` | Continuous 0-100% percentage slider with colored track |
| `ui/color_swatch_grid` | Grid of clickable predefined brand color swatches |
| `ui/key_recorder_input` | Hotkey and keyboard shortcut recorder field |
| `ui/text_counter_area` | Multiline textarea with live character countdown |

---

### 2. Navigation & Menus (45 Packages)
| Package | Description |
| :--- | :--- |
| `ui/sidebar_nav` | Collapsible modern vertical sidebar navigation |
| `ui/app_bar` | Top application bar with navigation icon, title, and action buttons |
| `ui/bottom_navigation` | Mobile bottom tab bar with animated icon switching |
| `ui/tab_bar` | Horizontal sliding tab bar with indicator underline |
| `ui/breadcrumb_trail` | Hierarchical path breadcrumbs with chevron separators |
| `ui/pagination_bar` | Numbered page switcher with previous/next and jump-to |
| `ui/drawer_menu` | Slide-out navigation drawer with user profile header |
| `ui/floating_action_menu` | Expandable floating action button (FAB) speed dial |
| `ui/mega_menu` | Multi-column desktop mega menu dropdown with categorized links |
| `ui/context_menu` | Right-click contextual popup menu with divider groups |
| `ui/stepper_nav` | Step-by-step wizard navigation with completed badges |
| `ui/dock_bar` | macOS-style floating dock bar with magnification effect |
| `ui/tree_view` | Collapsible folder and file hierarchy tree view |
| `ui/accordion_nav` | Multi-section vertical accordion with smooth expand/collapse |
| `ui/collapsible_menu` | Nested multi-level dropdown menu tree |
| `ui/rail_navigation` | Compact vertical icon rail for desktop dashboards |
| `ui/sub_navigation_bar` | Secondary horizontal sub-nav for deep page routes |
| `ui/page_header` | Standardized page header with title, subtitle, and breadcrumbs |
| `ui/command_palette` | Keyboard-driven Cmd+K / Ctrl+K search and action launcher |
| `ui/spotlight_search` | Floating modal overlay for global application searching |
| `ui/anchor_nav` | Sticky on-page table-of-contents anchor scroll navigation |
| `ui/tab_strip` | Browser-style draggable and closeable tab strip |
| `ui/jump_menu` | Quick-jump floating index for alphabetical lists |
| `ui/bottom_sheet_nav` | Swipeable bottom navigation sheet for mobile viewports |
| `ui/hamburger_button` | Animated morphing hamburger-to-close icon button |
| `ui/back_to_top_button` | Smooth scroll-to-top floating button with progress ring |
| `ui/infinite_breadcrumbs` | Auto-collapsing long breadcrumb path with ellipsis menu |
| `ui/segmented_tabs` | Pill-shaped segmented tabs for dashboard views |
| `ui/horizontal_scroll_menu`| Touch-friendly edge-fading horizontal scroll menu |
| `ui/vertical_steps` | Vertical checkout and onboarding progress step tracker |
| `ui/action_sheet` | iOS-style modal action sheet with cancel button |
| `ui/popup_bubble_menu` | Pointing bubble menu positioned relative to trigger element |
| `ui/navigation_pill` | Floating navigation capsule with glassmorphism blur |
| `ui/quick_links_bar` | Compact quick-access toolbar for tools and shortcuts |
| `ui/offcanvas_panel` | Full-height offcanvas sliding panel from left/right/top/bottom |
| `ui/split_button_menu` | Primary action button with secondary dropdown arrow |
| `ui/tab_carousel` | Swipeable tabbed container with touch gestures |
| `ui/nested_accordion` | Deeply nested multi-level expandable disclosure panels |
| `ui/sticky_nav_bar` | Top navigation bar that sticks on scroll with blur backdrop |
| `ui/swipeable_nav_tabs` | Touch swipe tabs with haptic feedback integration |
| `ui/header_search_combo` | Unified logo, global search, and user profile header |
| `ui/radial_menu` | Circular pie menu expanding around mouse cursor |
| `ui/footer_nav_grid` | Multi-column site footer with link sections and copyright |
| `ui/status_bar_hud` | Miniature system status and connectivity HUD strip |
| `ui/page_indicator_dots` | Pagination dot indicator with active pill animation |

---

### 3. Data Display, Tables & Grids (45 Packages)
| Package | Description |
| :--- | :--- |
| `ui/data_table` | High-performance sorting, filtering, and selectable data table |
| `ui/virtual_list` | Virtualized list renderer for 100,000+ items with zero lag |
| `ui/infinite_scroll_view` | Auto-fetching infinite scroll container with load trigger |
| `ui/tree_table` | Hierarchical expandable tree data table with indent guides |
| `ui/pivot_table` | Multi-dimensional pivot matrix with row/column groupings |
| `ui/timeline_view` | Vertical event timeline with dates, icons, and status badges |
| `ui/calendar_grid` | Monthly, weekly, and daily interactive calendar schedule grid |
| `ui/kanban_board` | Drag-and-drop Kanban workflow board with swimlanes and cards |
| `ui/gantt_chart` | Project management timeline chart with dependencies and milestones |
| `ui/matrix_grid` | N-by-N data matrix viewer with cell heatmap highlighting |
| `ui/badge_pill` | Notification counter and status tag badge with dot variant |
| `ui/avatar_group` | Overlapping circular user avatar group with counter overflow |
| `ui/chip_list` | Flowing list of interactive chips with delete and select states |
| `ui/stat_card` | Executive metric KPI card with sparkline and percentage change |
| `ui/kpi_metric` | Key performance indicator display with goal progress bar |
| `ui/comparison_table` | Feature matrix comparison table with checkmarks and tooltips |
| `ui/pricing_table` | Tiered subscription pricing cards with monthly/yearly toggle |
| `ui/feed_stream` | Social activity feed stream with avatar, timestamp, and actions |
| `ui/masonry_grid` | Pinterest-style dynamic multi-column masonry card grid |
| `ui/carousel_slider` | Touch swipeable media carousel with autoplay and arrows |
| `ui/card_deck` | Responsive deck of cards with consistent equal heights |
| `ui/waterfall_layout` | Dynamic cascading waterfall layout for variable height cards |
| `ui/key_value_table` | Clean two-column property-value inspector table |
| `ui/status_pill_badge` | Rounded status indicator with animated pulsing dot |
| `ui/user_profile_card` | Comprehensive user profile card with avatar, stats, bio |
| `ui/empty_state_view` | Illustrated empty state with call-to-action button |
| `ui/accordion_table` | Data table where rows expand into detailed nested views |
| `ui/column_toggle_table` | Data table with dynamic column visibility selector |
| `ui/exportable_table` | Data table with one-click CSV and JSON download buttons |
| `ui/filterable_cards` | Grid of cards filterable by category and search keyword |
| `ui/leaderboard_table` | Ranked gaming and sales leaderboard with trophy badges |
| `ui/audit_log_viewer` | Security and system event audit log with diff inspector |
| `ui/file_browser_grid` | Grid and list file manager with file type icons and sizes |
| `ui/comment_thread` | Nested hierarchical discussion comment thread with replies |
| `ui/changelog_list` | Software version changelog list with release badges |
| `ui/faq_accordion` | Frequently asked questions accordion with search highlight |
| `ui/shopping_cart_list` | E-commerce shopping bag list with thumbnail, price, delete |
| `ui/order_summary_card` | Checkout order receipt card with tax, shipping, total |
| `ui/invoice_display` | Professional invoice document view with line items and total |
| `ui/review_card` | Customer testimonial and review card with star rating and verified badge |
| `ui/media_list_item` | Media item with thumbnail, title, description, and metadata |
| `ui/rank_badge` | Gamified gold, silver, bronze ranking badge with ribbon |
| `ui/code_snippet_card` | Syntax-highlighted code snippet card with copy button |
| `ui/property_grid` | Visual grid of product specifications and technical details |
| `ui/activity_heatmap` | GitHub-style calendar contribution activity heatmap |

---

### 4. Data Visualization & Charts (40 Packages)
| Package | Description |
| :--- | :--- |
| `ui/chart_line` | Smooth curved and stepped multi-series line chart |
| `ui/chart_bar` | Vertical grouped and stacked multi-column bar chart |
| `ui/chart_horizontal_bar` | Horizontal ranked bar chart with value labels |
| `ui/chart_pie` | Multi-segment circular pie chart with hover explode effect |
| `ui/chart_donut` | Ring donut chart with centered aggregate total display |
| `ui/chart_area` | Gradient-filled multi-series area chart |
| `ui/chart_scatter` | Multi-variable 2D scatter plot with trendline |
| `ui/chart_bubble` | Three-dimensional data bubble chart with variable radiuses |
| `ui/chart_radar` | Spiderweb radar chart for multi-dimensional performance |
| `ui/chart_candlestick` | Financial stock candlestick chart with high/low/open/close |
| `ui/chart_gauge` | Semi-circular radial needle gauge with threshold color bands |
| `ui/chart_funnel` | Sales and conversion funnel pipeline visualization |
| `ui/chart_treemap` | Hierarchical nested rectangle treemap chart |
| `ui/chart_heatmap` | 2D color density heatmap matrix for intensity analysis |
| `ui/chart_sankey` | Flow diagram showing energy, traffic, and volume transfers |
| `ui/chart_sparkline` | Miniature inline trend chart with min/max highlight dots |
| `ui/chart_waterfall` | Positive and negative financial waterfall cumulative chart |
| `ui/chart_polar_area` | Polar area chart with equal-angle variable-radius sectors |
| `ui/chart_pyramid` | Population and hierarchical demographic pyramid chart |
| `ui/chart_bullet` | Performance target versus actual metric bullet chart |
| `ui/progress_ring` | Circular SVG progress ring with percentage readout |
| `ui/progress_bar` | Linear animated progress bar with gradient and striped styles |
| `ui/activity_gauge` | Apple Watch-style concentric circular fitness rings |
| `ui/speedometer_gauge` | Automotive-style high-precision dial speedometer |
| `ui/step_progress` | Multi-phase linear step progress tracker with checkmarks |
| `ui/liquid_fill_gauge` | Animated wave liquid fill water droplet gauge |
| `ui/meter_bar` | Hardware storage and battery meter bar with critical levels |
| `ui/range_gauge` | Min-max range gauge with colored safe/warning/critical zones |
| `ui/network_graph` | Node-link relational network topology graph with force physics |
| `ui/sunburst_chart` | Multi-level radial hierarchical sunburst diagram |
| `ui/venn_diagram` | Two-set and three-set overlapping Venn diagram |
| `ui/timeline_chart` | Horizontal chronological Gantt and milestone chart |
| `ui/box_plot` | Statistical five-number summary box and whisker plot |
| `ui/violin_plot` | Statistical kernel density violin plot with quartiles |
| `ui/word_cloud` | Frequency-weighted semantic word cloud layout |
| `ui/density_contour` | 2D elevation and mathematical density contour plot |
| `ui/multi_axis_chart` | Dual left-right Y-axis chart combining line and bar data |
| `ui/candlestick_mini` | Miniature trading chart preview for watchlists |
| `ui/metric_counter_clock`| Digital 7-segment LED style numeric counter clock |
| `ui/radial_bar_chart` | Concentric multi-colored radial bar chart |

---

### 5. Additional UI Categories (110 Packages)
Includes 35 Feedback/Modal packages, 35 Layouts/Containers packages, 30 Media/Audio/Video packages, 25 Gaming/Canvas packages, and 25 Theming/Utility packages.
All searchable via `star search ui/`.
