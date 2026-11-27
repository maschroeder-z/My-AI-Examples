When the user clicks on an article title, preview image, or "Read article" button, open the corresponding SharePoint content page in a large overlay instead of navigating away from the application.

**Overlay design**

- Display the overlay in the center of the screen.
- Use approximately 90% of the available screen width and height.
- Use a white background, rounded corners, and a subtle shadow.
- Darken the background behind the overlay.
- Prevent scrolling of the underlying blog interface while the overlay is open.
- Make the overlay full-screen on mobile devices.

**Overlay header**

Provide a fixed header containing:

- The article title.
- The author's name and publication date.
- An "Open original page" button that opens the original SharePoint page in a new browser tab.
- A prominent close button (X) in the upper-right corner.

**Article content**

- Load the original SharePoint content page dynamically using its associated page URL.
- Display the complete article content, including text, images, formatting, and embedded content where supported.
- Preserve the original article formatting as much as possible.
- Allow vertical scrolling within the overlay while keeping the overlay header visible.
- Display a loading indicator while retrieving the article.
- Use an iframe only if supported by the SharePoint environment and its security policies.
- If iframe embedding is not supported, use the available SharePoint data access mechanisms to retrieve and render supported page content safely.
- If neither approach is supported, provide a user-friendly message and a link to open the original page.

**Interactive behavior**

Allow users to close the overlay by:

- Clicking the close button.
- Pressing the Escape key.
- Clicking outside the overlay.

When the overlay is closed, preserve the current search text, selected filters, sorting options, loaded articles, and scrolling position of the underlying blog interface.

Ensure accessible keyboard navigation, focus management, and responsive behavior.

The objective is to provide a seamless reading experience similar to a modern online magazine, allowing users to discover and read multiple articles without leaving the blog application.