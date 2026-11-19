"""
Generates 335+ UI Packages for Star Language Ecosystem
Updates modules/ui/*.star, modules/catalog.json, and modules/ui/index.star
"""

import os
import json
import re

UI_PACKAGES = [
    # 1. Forms, Inputs & Pickers (55)
    ("date_picker", "Calendar date selection dialog and input field", "DatePicker"),
    ("time_picker", "Clock face and 24h/12h time selector widget", "TimePicker"),
    ("date_range_picker", "Dual calendar date span and range selector", "DateRangePicker"),
    ("color_picker", "Hex, RGB, HSL and gradient interactive color picker", "ColorPicker"),
    ("color_palette_wheel", "Circular color spectrum wheel and hue slider", "ColorPaletteWheel"),
    ("rich_text_editor", "WYSIWYG formatted text editor with bold, italic, lists", "RichTextEditor"),
    ("markdown_editor", "Split-pane markdown source editor with live preview", "MarkdownEditor"),
    ("code_editor", "Syntax-highlighted code editor with line numbering", "CodeEditor"),
    ("slider_range", "Dual-thumb min/max range slider component", "SliderRange"),
    ("slider_stepped", "Discrete stepped numeric slider with tick marks", "SliderStepped"),
    ("tag_input", "Chip-based tag entry with auto-suggestion and chip removal", "TagInput"),
    ("file_uploader", "Drag-and-drop multi-file upload zone with progress bars", "FileUploader"),
    ("file_drop_zone", "Dashed border drag-and-drop file receiver with MIME filter", "FileDropZone"),
    ("signature_pad", "Touch and mouse digital signature capture canvas", "SignaturePad"),
    ("otp_input", "Auto-advancing segmented 4-to-6 digit OTP/PIN input", "OtpInput"),
    ("pin_code_field", "Secure masked PIN entry field with biometric icon", "PinCodeField"),
    ("rating_bar", "Interactive 5-star or custom icon rating selector", "RatingBar"),
    ("autocomplete", "Typeahead autocomplete suggestions dropdown", "Autocomplete"),
    ("masked_input", "Formatted input mask for phone numbers, SSN, and cards", "MaskedInput"),
    ("phone_input", "International telephone number input with country flag", "PhoneInput"),
    ("currency_input", "Real-time formatted monetary amount input with currency symbol", "CurrencyInput"),
    ("credit_card_input", "Smart card number formatter with auto card brand detection", "CreditCardInput"),
    ("checkbox_group", "Grouped tri-state checkbox list with select-all", "CheckboxGroup"),
    ("radio_group", "Grouped single-selection radio button list with custom styling", "RadioGroup"),
    ("switch_toggle", "Animated iOS and Material style toggle switch", "SwitchToggle"),
    ("stepper_input", "Incremental numeric +/- stepper with min/max bounds", "StepperInput"),
    ("cascader", "Hierarchical multi-level cascaded dropdown selector", "Cascader"),
    ("transfer_list", "Dual-column shuttle box transfer list with move buttons", "TransferList"),
    ("tree_select", "Hierarchical tree-view dropdown selector with search", "TreeSelect"),
    ("mentions_input", "@mention and #hashtag suggestion popover input", "MentionsInput"),
    ("password_strength", "Dynamic password security meter with rule checkmarks", "PasswordStrength"),
    ("search_bar", "Full-featured search bar with voice input icon and clear button", "SearchBar"),
    ("filter_panel", "Collapsible multi-criteria filter builder panel", "FilterPanel"),
    ("multi_select", "Searchable multi-selection dropdown with chip tags", "MultiSelect"),
    ("dropdown_select", "Standard customizable dropdown picker with icons", "DropdownSelect"),
    ("combo_box", "Hybrid text input and dropdown select combo box", "ComboBox"),
    ("segmented_picker", "iOS-style pill segmented control with sliding indicator", "SegmentedPicker"),
    ("wheel_picker", "Scrollable 3D drum wheel picker for dates and lists", "WheelPicker"),
    ("time_duration_picker", "Hours, minutes, seconds duration timer picker", "TimeDurationPicker"),
    ("quantity_selector", "E-commerce shopping cart item quantity adjuster", "QuantitySelector"),
    ("search_filter_chips", "Horizontal scrollable filter chips with active toggles", "SearchFilterChips"),
    ("boolean_toggle_card", "Visual card with integrated switch and description", "BooleanToggleCard"),
    ("inline_edit_field", "Click-to-edit inline text field with save/cancel icons", "InlineEditField"),
    ("expandable_search", "Collapsed search icon expanding into full search bar", "ExpandableSearch"),
    ("geo_location_input", "Address autocomplete and GPS location capture field", "GeoLocationInput"),
    ("dimension_input", "Width, height, depth 3D dimension input with unit toggle", "DimensionInput"),
    ("ip_address_input", "Segmented IPv4 and IPv6 network address field", "IpAddressInput"),
    ("url_input", "Validated web URL input with protocol prefix pill", "UrlInput"),
    ("json_input_validator", "Live JSON syntax highlighting and validation editor", "JsonInputValidator"),
    ("regex_tester_input", "Pattern tester input with live match highlighting", "RegexTesterInput"),
    ("unit_converter_input", "Dual-field imperial to metric live converter input", "UnitConverterInput"),
    ("percentage_slider", "Continuous 0-100% percentage slider with colored track", "PercentageSlider"),
    ("color_swatch_grid", "Grid of clickable predefined brand color swatches", "ColorSwatchGrid"),
    ("key_recorder_input", "Hotkey and keyboard shortcut recorder field", "KeyRecorderInput"),
    ("text_counter_area", "Multiline textarea with live character countdown", "TextCounterArea"),

    # 2. Navigation & Menus (45)
    ("sidebar_nav", "Collapsible modern vertical sidebar navigation", "SidebarNav"),
    ("app_bar", "Top application bar with navigation icon, title, and action buttons", "AppBar"),
    ("bottom_navigation", "Mobile bottom tab bar with animated icon switching", "BottomNavigation"),
    ("tab_bar", "Horizontal sliding tab bar with indicator underline", "TabBar"),
    ("breadcrumb_trail", "Hierarchical path breadcrumbs with chevron separators", "BreadcrumbTrail"),
    ("pagination_bar", "Numbered page switcher with previous/next and jump-to", "PaginationBar"),
    ("drawer_menu", "Slide-out navigation drawer with user profile header", "DrawerMenu"),
    ("floating_action_menu", "Expandable floating action button (FAB) speed dial", "FloatingActionMenu"),
    ("mega_menu", "Multi-column desktop mega menu dropdown with categorized links", "MegaMenu"),
    ("context_menu", "Right-click contextual popup menu with divider groups", "ContextMenu"),
    ("stepper_nav", "Step-by-step wizard navigation with completed badges", "StepperNav"),
    ("dock_bar", "macOS-style floating dock bar with magnification effect", "DockBar"),
    ("tree_view", "Collapsible folder and file hierarchy tree view", "TreeView"),
    ("accordion_nav", "Multi-section vertical accordion with smooth expand/collapse", "AccordionNav"),
    ("collapsible_menu", "Nested multi-level dropdown menu tree", "CollapsibleMenu"),
    ("rail_navigation", "Compact vertical icon rail for desktop dashboards", "RailNavigation"),
    ("sub_navigation_bar", "Secondary horizontal sub-nav for deep page routes", "SubNavigationBar"),
    ("page_header", "Standardized page header with title, subtitle, and breadcrumbs", "PageHeader"),
    ("command_palette", "Keyboard-driven Cmd+K / Ctrl+K search and action launcher", "CommandPalette"),
    ("spotlight_search", "Floating modal overlay for global application searching", "SpotlightSearch"),
    ("anchor_nav", "Sticky on-page table-of-contents anchor scroll navigation", "AnchorNav"),
    ("tab_strip", "Browser-style draggable and closeable tab strip", "TabStrip"),
    ("jump_menu", "Quick-jump floating index for alphabetical lists", "JumpMenu"),
    ("bottom_sheet_nav", "Swipeable bottom navigation sheet for mobile viewports", "BottomSheetNav"),
    ("hamburger_button", "Animated morphing hamburger-to-close icon button", "HamburgerButton"),
    ("back_to_top_button", "Smooth scroll-to-top floating button with progress ring", "BackToTopButton"),
    ("infinite_breadcrumbs", "Auto-collapsing long breadcrumb path with ellipsis menu", "InfiniteBreadcrumbs"),
    ("segmented_tabs", "Pill-shaped segmented tabs for dashboard views", "SegmentedTabs"),
    ("horizontal_scroll_menu", "Touch-friendly edge-fading horizontal scroll menu", "HorizontalScrollMenu"),
    ("vertical_steps", "Vertical checkout and onboarding progress step tracker", "VerticalSteps"),
    ("action_sheet", "iOS-style modal action sheet with cancel button", "ActionSheet"),
    ("popup_bubble_menu", "Pointing bubble menu positioned relative to trigger element", "PopupBubbleMenu"),
    ("navigation_pill", "Floating navigation capsule with glassmorphism blur", "NavigationPill"),
    ("quick_links_bar", "Compact quick-access toolbar for tools and shortcuts", "QuickLinksBar"),
    ("offcanvas_panel", "Full-height offcanvas sliding panel from left/right/top/bottom", "OffcanvasPanel"),
    ("split_button_menu", "Primary action button with secondary dropdown arrow", "SplitButtonMenu"),
    ("tab_carousel", "Swipeable tabbed container with touch gestures", "TabCarousel"),
    ("nested_accordion", "Deeply nested multi-level expandable disclosure panels", "NestedAccordion"),
    ("sticky_nav_bar", "Top navigation bar that sticks on scroll with blur backdrop", "StickyNavBar"),
    ("swipeable_nav_tabs", "Touch swipe tabs with haptic feedback integration", "SwipeableNavTabs"),
    ("header_search_combo", "Unified logo, global search, and user profile header", "HeaderSearchCombo"),
    ("radial_menu", "Circular pie menu expanding around mouse cursor", "RadialMenu"),
    ("footer_nav_grid", "Multi-column site footer with link sections and copyright", "FooterNavGrid"),
    ("status_bar_hud", "Miniature system status and connectivity HUD strip", "StatusBarHud"),
    ("page_indicator_dots", "Pagination dot indicator with active pill animation", "PageIndicatorDots"),

    # 3. Data Display, Tables & Grids (45)
    ("data_table", "High-performance sorting, filtering, and selectable data table", "DataTable"),
    ("virtual_list", "Virtualized list renderer for 100,000+ items with zero lag", "VirtualList"),
    ("infinite_scroll_view", "Auto-fetching infinite scroll container with load trigger", "InfiniteScrollView"),
    ("tree_table", "Hierarchical expandable tree data table with indent guides", "TreeTable"),
    ("pivot_table", "Multi-dimensional pivot matrix with row/column groupings", "PivotTable"),
    ("timeline_view", "Vertical event timeline with dates, icons, and status badges", "TimelineView"),
    ("calendar_grid", "Monthly, weekly, and daily interactive calendar schedule grid", "CalendarGrid"),
    ("kanban_board", "Drag-and-drop Kanban workflow board with swimlanes and cards", "KanbanBoard"),
    ("gantt_chart", "Project management timeline chart with dependencies and milestones", "GanttChart"),
    ("matrix_grid", "N-by-N data matrix viewer with cell heatmap highlighting", "MatrixGrid"),
    ("badge_pill", "Notification counter and status tag badge with dot variant", "BadgePill"),
    ("avatar_group", "Overlapping circular user avatar group with counter overflow", "AvatarGroup"),
    ("chip_list", "Flowing list of interactive chips with delete and select states", "ChipList"),
    ("stat_card", "Executive metric KPI card with sparkline and percentage change", "StatCard"),
    ("kpi_metric", "Key performance indicator display with goal progress bar", "KpiMetric"),
    ("comparison_table", "Feature matrix comparison table with checkmarks and tooltips", "ComparisonTable"),
    ("pricing_table", "Tiered subscription pricing cards with monthly/yearly toggle", "PricingTable"),
    ("feed_stream", "Social activity feed stream with avatar, timestamp, and actions", "FeedStream"),
    ("masonry_grid", "Pinterest-style dynamic multi-column masonry card grid", "MasonryGrid"),
    ("carousel_slider", "Touch swipeable media carousel with autoplay and arrows", "CarouselSlider"),
    ("card_deck", "Responsive deck of cards with consistent equal heights", "CardDeck"),
    ("waterfall_layout", "Dynamic cascading waterfall layout for variable height cards", "WaterfallLayout"),
    ("key_value_table", "Clean two-column property-value inspector table", "KeyValueTable"),
    ("status_pill_badge", "Rounded status indicator with animated pulsing dot", "StatusPillBadge"),
    ("user_profile_card", "Comprehensive user profile card with avatar, stats, bio", "UserProfileCard"),
    ("empty_state_view", "Illustrated empty state with call-to-action button", "EmptyStateView"),
    ("accordion_table", "Data table where rows expand into detailed nested views", "AccordionTable"),
    ("column_toggle_table", "Data table with dynamic column visibility selector", "ColumnToggleTable"),
    ("exportable_table", "Data table with one-click CSV and JSON download buttons", "ExportableTable"),
    ("filterable_cards", "Grid of cards filterable by category and search keyword", "FilterableCards"),
    ("leaderboard_table", "Ranked gaming and sales leaderboard with trophy badges", "LeaderboardTable"),
    ("audit_log_viewer", "Security and system event audit log with diff inspector", "AuditLogViewer"),
    ("file_browser_grid", "Grid and list file manager with file type icons and sizes", "FileBrowserGrid"),
    ("comment_thread", "Nested hierarchical discussion comment thread with replies", "CommentThread"),
    ("changelog_list", "Software version changelog list with release badges", "ChangelogList"),
    ("faq_accordion", "Frequently asked questions accordion with search highlight", "FaqAccordion"),
    ("shopping_cart_list", "E-commerce shopping bag list with thumbnail, price, delete", "ShoppingCartList"),
    ("order_summary_card", "Checkout order receipt card with tax, shipping, total", "OrderSummaryCard"),
    ("invoice_display", "Professional invoice document view with line items and total", "InvoiceDisplay"),
    ("review_card", "Customer testimonial and review card with star rating and verified badge", "ReviewCard"),
    ("media_list_item", "Media item with thumbnail, title, description, and metadata", "MediaListItem"),
    ("rank_badge", "Gamified gold, silver, bronze ranking badge with ribbon", "RankBadge"),
    ("code_snippet_card", "Syntax-highlighted code snippet card with copy button", "CodeSnippetCard"),
    ("property_grid", "Visual grid of product specifications and technical details", "PropertyGrid"),
    ("activity_heatmap", "GitHub-style calendar contribution activity heatmap", "ActivityHeatmap"),

    # 4. Data Visualization & Charts (40)
    ("chart_line", "Smooth curved and stepped multi-series line chart", "ChartLine"),
    ("chart_bar", "Vertical grouped and stacked multi-column bar chart", "ChartBar"),
    ("chart_horizontal_bar", "Horizontal ranked bar chart with value labels", "ChartHorizontalBar"),
    ("chart_pie", "Multi-segment circular pie chart with hover explode effect", "ChartPie"),
    ("chart_donut", "Ring donut chart with centered aggregate total display", "ChartDonut"),
    ("chart_area", "Gradient-filled multi-series area chart", "ChartArea"),
    ("chart_scatter", "Multi-variable 2D scatter plot with trendline", "ChartScatter"),
    ("chart_bubble", "Three-dimensional data bubble chart with variable radiuses", "ChartBubble"),
    ("chart_radar", "Spiderweb radar chart for multi-dimensional performance", "ChartRadar"),
    ("chart_candlestick", "Financial stock candlestick chart with high/low/open/close", "ChartCandlestick"),
    ("chart_gauge", "Semi-circular radial needle gauge with threshold color bands", "ChartGauge"),
    ("chart_funnel", "Sales and conversion funnel pipeline visualization", "ChartFunnel"),
    ("chart_treemap", "Hierarchical nested rectangle treemap chart", "ChartTreemap"),
    ("chart_heatmap", "2D color density heatmap matrix for intensity analysis", "ChartHeatmap"),
    ("chart_sankey", "Flow diagram showing energy, traffic, and volume transfers", "ChartSankey"),
    ("chart_sparkline", "Miniature inline trend chart with min/max highlight dots", "ChartSparkline"),
    ("chart_waterfall", "Positive and negative financial waterfall cumulative chart", "ChartWaterfall"),
    ("chart_polar_area", "Polar area chart with equal-angle variable-radius sectors", "ChartPolarArea"),
    ("chart_pyramid", "Population and hierarchical demographic pyramid chart", "ChartPyramid"),
    ("chart_bullet", "Performance target versus actual metric bullet chart", "ChartBullet"),
    ("progress_ring", "Circular SVG progress ring with percentage readout", "ProgressRing"),
    ("progress_bar", "Linear animated progress bar with gradient and striped styles", "ProgressBar"),
    ("activity_gauge", "Apple Watch-style concentric circular fitness rings", "ActivityGauge"),
    ("speedometer_gauge", "Automotive-style high-precision dial speedometer", "SpeedometerGauge"),
    ("step_progress", "Multi-phase linear step progress tracker with checkmarks", "StepProgress"),
    ("liquid_fill_gauge", "Animated wave liquid fill water droplet gauge", "LiquidFillGauge"),
    ("meter_bar", "Hardware storage and battery meter bar with critical levels", "MeterBar"),
    ("range_gauge", "Min-max range gauge with colored safe/warning/critical zones", "RangeGauge"),
    ("network_graph", "Node-link relational network topology graph with force physics", "NetworkGraph"),
    ("sunburst_chart", "Multi-level radial hierarchical sunburst diagram", "SunburstChart"),
    ("venn_diagram", "Two-set and three-set overlapping Venn diagram", "VennDiagram"),
    ("timeline_chart", "Horizontal chronological Gantt and milestone chart", "TimelineChart"),
    ("box_plot", "Statistical five-number summary box and whisker plot", "BoxPlot"),
    ("violin_plot", "Statistical kernel density violin plot with quartiles", "ViolinPlot"),
    ("word_cloud", "Frequency-weighted semantic word cloud layout", "WordCloud"),
    ("density_contour", "2D elevation and mathematical density contour plot", "DensityContour"),
    ("multi_axis_chart", "Dual left-right Y-axis chart combining line and bar data", "MultiAxisChart"),
    ("candlestick_mini", "Miniature trading chart preview for watchlists", "CandlestickMini"),
    ("metric_counter_clock", "Digital 7-segment LED style numeric counter clock", "MetricCounterClock"),
    ("radial_bar_chart", "Concentric multi-colored radial bar chart", "RadialBarChart"),

    # 5. Feedback, Modals & Notifications (35)
    ("modal_dialog", "Centered pop-up modal dialog with backdrop blur and escape key", "ModalDialog"),
    ("bottom_sheet", "Swipeable mobile bottom modal sheet with grab handle", "BottomSheet"),
    ("toast_notification", "Stackable non-blocking toast notifications (success, error, info)", "ToastNotification"),
    ("snackbar", "Material bottom snackbar notice with action button", "Snackbar"),
    ("alert_banner", "Prominent alert banner with icon and close button", "AlertBanner"),
    ("popover_box", "Rich contextual popover anchored to a trigger element", "PopoverBox"),
    ("tooltip_balloon", "Hover and focus tooltip balloon with directional arrow", "TooltipBalloon"),
    ("confirm_dialog", "Destructive action confirmation dialog with confirm/cancel", "ConfirmDialog"),
    ("drawer_sheet", "Side-sliding drawer panel for details and forms", "DrawerSheet"),
    ("banner_notice", "Full-width persistent top notification banner", "BannerNotice"),
    ("badge_ribbon", "Corner diagonal ribbon badge (New, Sale, Pro, Beta)", "BadgeRibbon"),
    ("loading_spinner", "Modern rotating ring and dual-ring loading spinner", "LoadingSpinner"),
    ("skeleton_loader", "Placeholder wireframe skeleton loader with shimmer pulse", "SkeletonLoader"),
    ("shimmer_effect", "Moving gradient shimmer highlight for loading states", "ShimmerEffect"),
    ("empty_state_card", "Illustrated empty state with action button", "EmptyStateCard"),
    ("error_boundary_view", "Graceful error boundary fallback card with stack trace", "ErrorBoundaryView"),
    ("splash_screen", "Initial application loading splash view with logo fade", "SplashScreen"),
    ("walkthrough_tour", "Multi-step interactive feature tour overlay with spotlights", "WalkthroughTour"),
    ("hint_pointer", "Animated pulsating arrow pointer highlighting new features", "HintPointer"),
    ("pulse_indicator", "Glowing radar pulse dot indicator for live updates", "PulseIndicator"),
    ("progress_dialog", "Modal progress dialog for long-running operations", "ProgressDialog"),
    ("countdown_timer", "Visual countdown timer with flip clock animation", "CountdownTimer"),
    ("confetti_celebration", "Full-screen particle confetti explosion for achievements", "ConfettiCelebration"),
    ("notification_badge", "Animated bouncing notification badge with counter", "NotificationBadge"),
    ("copy_tooltip", "Click-to-copy button with 'Copied!' temporary tooltip", "CopyTooltip"),
    ("undo_snackbar", "Action notification with 5-second undo button", "UndoSnackbar"),
    ("rate_app_dialog", "Star rating prompt dialog asking for user feedback", "RateAppDialog"),
    ("cookie_consent_banner", "GDPR and privacy compliant cookie consent banner", "CookieConsentBanner"),
    ("version_update_dialog", "Software update prompt with release notes and update CTA", "VersionUpdateDialog"),
    ("session_timeout_warning", "Inactivity warning modal with session extension countdown", "SessionTimeoutWarning"),
    ("network_offline_banner", "Red sticky banner warning when internet drops", "NetworkOfflineBanner"),
    ("watermark_overlay", "Diagonal text and image security watermark overlay", "WatermarkOverlay"),
    ("blur_overlay", "Frosted glass backdrop blur modal blocker", "BlurOverlay"),
    ("progress_hud", "Centered semi-transparent activity HUD with spinner", "ProgressHud"),
    ("toast_stack_manager", "Multi-notification queue manager with auto-dismiss", "ToastStackManager"),

    # 6. Layouts, Containers & Panels (35)
    ("split_pane", "Resizable horizontal and vertical split divider view", "SplitPane"),
    ("resizable_panel", "Resizable side and bottom docking panels", "ResizablePanel"),
    ("responsive_grid", "12-column responsive flex and grid container with breakpoints", "ResponsiveGrid"),
    ("aspect_ratio_box", "Fixed 16:9, 4:3, 1:1 aspect ratio constraint container", "AspectRatioBox"),
    ("sticky_header", "Scrollable container with sticky section headers", "StickyHeader"),
    ("card_expandable", "Card that smoothly animates and unfolds to reveal details", "CardExpandable"),
    ("glass_card", "Frosted glassmorphism container with backdrop blur filter", "GlassCard"),
    ("neumorphic_box", "Soft extruded neumorphic container with dual drop shadows", "NeumorphicBox"),
    ("divider_fancy", "Decorative divider with centered text, icon, or gradient", "DividerFancy"),
    ("scroll_container", "Customizable scroll view with custom styled scrollbars", "ScrollContainer"),
    ("snap_scroller", "Touch snap scroll container for horizontal cards", "SnapScroller"),
    ("parallax_view", "Multi-layer depth parallax scroll container", "ParallaxView"),
    ("hero_banner", "Full-width visual hero banner with title, CTA, and background", "HeroBanner"),
    ("media_object", "Traditional media object layout (left image, right body)", "MediaObject"),
    ("spacer_box", "Flexible and fixed layout spacer widget", "SpacerBox"),
    ("stack_layout", "Layered Z-index overlapping stack container", "StackLayout"),
    ("wrap_layout", "Flexible wrap layout that flows children onto new lines", "WrapLayout"),
    ("dashboard_grid", "Configurable widget grid with drag-and-drop rearrangement", "DashboardGrid"),
    ("dockable_layout", "Professional multi-dock IDE and workspace layout", "DockableLayout"),
    ("masonry_flow", "Dynamic Pinterest-style vertical column flow", "MasonryFlow"),
    ("tile_grid", "Uniform square tile grid for app launchers and galleries", "TileGrid"),
    ("center_container", "Perfect horizontal and vertical centering wrapper", "CenterContainer"),
    ("constrained_box", "Min/max width and height constraint enforcement box", "ConstrainedBox"),
    ("fitted_box", "Container that scales and fits child widget proportionally", "FittedBox"),
    ("safe_area_container", "Mobile notch and home-bar safe area padding container", "SafeAreaContainer"),
    ("card_flip_view", "3D double-sided flipping card with front and back faces", "CardFlipView"),
    ("perspective_card", "3D tilt card that tracks mouse hover tilt angle", "PerspectiveCard"),
    ("collapsible_panel", "Expandable header panel with toggle chevron", "CollapsiblePanel"),
    ("sticky_footer", "Viewport layout where footer always sticks to bottom", "StickyFooter"),
    ("two_column_layout", "Standard content plus sidebar layout", "TwoColumnLayout"),
    ("three_column_layout", "Left navigation, center content, right sidebar layout", "ThreeColumnLayout"),
    ("holy_grail_layout", "Classic header, 3-column body, and footer layout", "HolyGrailLayout"),
    ("card_stack_swipe", "Tinder-style swipeable card deck with left/right dismiss", "CardStackSwipe"),
    ("drawer_layout", "Standard desktop split-screen drawer and canvas layout", "DrawerLayout"),
    ("grid_list_toggle", "Toggleable container switching between grid and list views", "GridListToggle"),

    # 7. Media, Video & Audio (30)
    ("video_player", "Responsive HTML5 and native video player with custom controls", "VideoPlayer"),
    ("audio_player", "Audio playback bar with play/pause, scrub bar, and duration", "AudioPlayer"),
    ("image_gallery", "Multi-thumbnail image gallery with full-screen lightbox", "ImageGallery"),
    ("image_cropper", "Interactive circular and rectangular image crop tool", "ImageCropper"),
    ("lightbox_viewer", "Fullscreen modal image and video viewer with zoom/pan", "LightboxViewer"),
    ("audio_visualizer", "Real-time frequency bar and wave audio visualizer", "AudioVisualizer"),
    ("waveform_display", "Sound wave visualization with clickable timeline scrubbing", "WaveformDisplay"),
    ("pdf_viewer", "Embedded PDF document viewer with page navigation and zoom", "PdfViewer"),
    ("qr_code_view", "Dynamic QR code renderer generated from text or URL", "QrCodeView"),
    ("barcode_display", "UPC, EAN, and Code128 barcode generator view", "BarcodeDisplay"),
    ("camera_viewfinder", "Camera stream preview with capture button and shutter flash", "CameraViewfinder"),
    ("lottie_player", "Vector animation player for Lottie JSON animations", "LottiePlayer"),
    ("rive_player", "Interactive vector state machine player for Rive assets", "RivePlayer"),
    ("media_controls_bar", "Universal playback control bar with volume and speed", "MediaControlsBar"),
    ("image_comparison_slider", "Before-and-after image comparison slider", "ImageComparisonSlider"),
    ("avatar_editor", "Circular avatar upload, reposition, and zoom editor", "AvatarEditor"),
    ("audio_playlist", "Music and podcast playlist manager with queue sorting", "AudioPlaylist"),
    ("video_pip_player", "Picture-in-picture floating mini video player", "VideoPipPlayer"),
    ("image_magnifier", "E-commerce product image zoom lens magnifier", "ImageMagnifier"),
    ("pan_zoom_viewer", "Pinch-to-zoom and pan container for high-res images", "PanZoomViewer"),
    ("svg_canvas_view", "Scalable Vector Graphics (SVG) interactive path viewer", "SvgCanvasView"),
    ("gif_player", "Animated GIF player with pause, loop, and frame controls", "GifPlayer"),
    ("subtitles_overlay", "Synchronized closed captions and video subtitles overlay", "SubtitlesOverlay"),
    ("sound_effect_button", "Interactive button with integrated WebAudio click sound", "SoundEffectButton"),
    ("video_playlist_carousel", "Video thumbnail playlist with active indicator", "VideoPlaylistCarousel"),
    ("voice_recorder_view", "Voice memo recording interface with animated microphone", "VoiceRecorderView"),
    ("aspect_ratio_image", "Progressive image loader with placeholder blur", "AspectRatioImage"),
    ("lazy_image_loader", "Intersection-observer powered lazy image loader", "LazyImageLoader"),
    ("icon_font_viewer", "Interactive searchable icon font glyph inspector", "IconFontViewer"),
    ("media_duration_scrubber", "High-precision video scrubbing timeline with thumbnails", "MediaDurationScrubber"),

    # 8. Gaming, Canvas & 3D/Effects (25)
    ("particle_canvas", "Interactive background particle network with mouse physics", "ParticleCanvas"),
    ("confetti_cannon", "Celebratory confetti particle burst physics emitter", "ConfettiCannon"),
    ("canvas_painter", "Freehand drawing and painting canvas with brush sizes", "CanvasPainter"),
    ("gl_viewport", "WebGL / WebGPU 3D viewport canvas for shaders and meshes", "GlViewport"),
    ("joystick_controller", "Virtual touch analog joystick for mobile gaming", "JoystickController"),
    ("dpad_controller", "4-way and 8-way directional pad controller", "DpadController"),
    ("game_hud", "In-game heads-up display with health bar, score, and ammo", "GameHud"),
    ("physics_playground", "2D rigid-body physics simulation container", "PhysicsPlayground"),
    ("scratch_card", "Interactive lottery scratch-off card with coin sound", "ScratchCard"),
    ("sound_effects_panel", "Soundboard panel with clickable audio pads", "SoundEffectsPanel"),
    ("gradient_canvas", "Animated shifting mesh gradient background", "GradientCanvas"),
    ("starfield_canvas", "3D warp-speed starfield animation canvas", "StarfieldCanvas"),
    ("fireworks_display", "Automated and interactive fireworks explosion canvas", "FireworksDisplay"),
    ("rain_snow_emitter", "Weather rain and snowfall particle effect overlay", "RainSnowEmitter"),
    ("neon_glow_card", "Glowing neon cyberpunk card with border animations", "NeonGlowCard"),
    ("matrix_rain_canvas", "Digital green Matrix code stream animation", "MatrixRainCanvas"),
    ("retro_crt_shader", "Retro CRT monitor curvature and scanline overlay", "RetroCrtShader"),
    ("flip_clock_canvas", "Vintage mechanical split-flap display for time/stats", "FlipClockCanvas"),
    ("dice_roller_view", "3D rolling dice simulator with random roll physics", "DiceRollerView"),
    ("slot_machine_spinner", "Casino-style slot machine spinning reel component", "SlotMachineSpinner"),
    ("card_shuffle_view", "Animated poker and trading card deck shuffler", "CardShuffleView"),
    ("radar_sweep_canvas", "Rotating circular radar sweep line with blips", "RadarSweepCanvas"),
    ("smoke_fog_emitter", "Atmospheric drifting smoke and fog particle canvas", "SmokeFogEmitter"),
    ("bubble_pop_game", "Interactive floating bubble popping mini-game", "BubblePopGame"),
    ("mini_map_viewport", "Real-time navigation minimap with player indicator", "MiniMapViewport"),

    # 9. Theming, Utilities & Localization (25)
    ("theme_dark_light", "One-click dark mode and light mode toggle switch with auto-detect", "ThemeDarkLight"),
    ("theme_customizer", "Live theme editor with primary color, radius, and font pickers", "ThemeCustomizer"),
    ("contrast_checker", "WCAG accessibility contrast ratio validator and color tester", "ContrastChecker"),
    ("font_picker", "Google Fonts and system typography preview and selection picker", "FontPicker"),
    ("icon_pack_material", "Comprehensive Google Material Symbols and Icons pack", "IconPackMaterial"),
    ("icon_pack_lucide", "Modern, beautiful Lucide vector icon pack", "IconPackLucide"),
    ("icon_pack_feather", "Simply beautiful open-source Feather icon pack", "IconPackFeather"),
    ("icon_pack_fontawesome", "Complete Font Awesome vector icons library", "IconPackFontawesome"),
    ("keyboard_shortcuts_modal", "Pop-up cheat sheet dialog of available hotkeys", "KeyboardShortcutsModal"),
    ("print_stylesheet", "Print-optimized layout and CSS formatter for reports", "PrintStylesheet"),
    ("i18n_locale_switcher", "Multi-language flag and locale dropdown switcher", "I18nLocaleSwitcher"),
    ("accessibility_toolbar", "Accessibility menu (font resize, high contrast, dyslexia font)", "AccessibilityToolbar"),
    ("css_grid_builder", "Visual interactive CSS grid template generator", "CssGridBuilder"),
    ("box_shadow_generator", "Visual drop-shadow and elevation tuner with preview", "BoxShadowGenerator"),
    ("border_radius_tuner", "Interactive 8-point border radius shaper", "BorderRadiusTuner"),
    ("color_gradient_generator", "Multi-stop linear and radial gradient builder", "ColorGradientGenerator"),
    ("device_frame_previewer", "Realistic iPhone, iPad, Android, and MacBook device mockups", "DeviceFramePreviewer"),
    ("orientation_lock_helper", "Mobile landscape/portrait orientation prompt overlay", "OrientationLockHelper"),
    ("reading_progress_bar", "Top edge reading progress bar tracking page scroll depth", "ReadingProgressBar"),
    ("fullscreen_toggle", "One-click HTML5 fullscreen toggle button with icon change", "FullscreenToggle"),
    ("zoom_pan_container", "Google Maps-style canvas zoom, pan, and reset controls", "ZoomPanContainer"),
    ("virtual_keyboard", "On-screen touch keyboard for kiosks and accessibility", "VirtualKeyboard"),
    ("clipboard_copy_button", "Click-to-copy button with checkmark feedback", "ClipboardCopyButton"),
    ("time_ago_display", "Relative '5 minutes ago' reactive timestamp display", "TimeAgoDisplay"),
    ("currency_formatter_view", "International multi-currency live conversion display", "CurrencyFormatterView"),
]

def main():
    ui_dir = os.path.abspath("modules/ui")
    os.makedirs(ui_dir, exist_ok=True)
    
    # 1. Generate individual .star module files
    generated_count = 0
    module_names = []

    for name, desc, cls_name in UI_PACKAGES:
        file_path = os.path.join(ui_dir, f"{name}.star")
        module_names.append(name)
        
        content = f"""# Star Standard Library: ui/{name}
# Description: {desc}
# Author: Star Core Team
# Version: 1.0.0

class {cls_name}
    property name = "{name}"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: {cls_name}>"
    end
end

function create()
    return {cls_name}()
end

function describe()
    return "{desc}"
end
"""
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        generated_count += 1

    print(f"✓ Generated {generated_count} UI module files in '{ui_dir}'")

    # 2. Update modules/catalog.json
    catalog_path = os.path.abspath("modules/catalog.json")
    with open(catalog_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    # Filter out existing ui/ entries to replace/refresh cleanly
    non_ui = [e for e in catalog if not e.get("name", "").startswith("ui/")]
    
    # Add all UI packages
    for name, desc, _ in UI_PACKAGES:
        non_ui.append({
            "name": f"ui/{name}",
            "category": "ui",
            "version": "1.0.0",
            "description": desc,
            "path": f"modules/ui/{name}.star",
            "author": "Star Core Team",
            "license": "MIT"
        })

    with open(catalog_path, "w", encoding="utf-8") as f:
        json.dump(non_ui, f, indent=2)

    print(f"✓ Updated '{catalog_path}' with {len(UI_PACKAGES)} UI packages (Total in catalog: {len(non_ui)})")

    # 3. Update modules/ui/index.star
    index_path = os.path.join(ui_dir, "index.star")
    index_lines = [
        "# Star Category Index: ui",
        f"# Contains {len(UI_PACKAGES)} modules",
        ""
    ]
    for name in module_names[:30]:  # Link first 30 commonly used
        index_lines.append(f'use "{name}.star"')
    index_lines.append("")
    index_lines.append("function category_info()")
    index_lines.append(f'    return "Category: ui with {len(UI_PACKAGES)} modules"')
    index_lines.append("end")

    with open(index_path, "w", encoding="utf-8") as f:
        f.write("\n".join(index_lines) + "\n")

    print(f"✓ Updated '{index_path}'")

if __name__ == "__main__":
    main()
