// formatBotReply.js

/**
 * Formats a raw bot reply string into HTML for display.
 * Supports a simplified Markdown-like syntax:
 * - **Bold**: `**text**` or `*text*`
 * - *Italics*: `_text_` or `*text*` (if not already bolded by `**`)
 * - Code (inline): `` `code` ``
 * - Code (block):
 * ```
 * your code here
 * ```
 * - Unordered Lists: Lines starting with `* ` or `- `
 * - Paragraphs: Automatically handles double newlines.
 *
 * @param {string} rawText The unformatted string received from the bot.
 * @returns {string} The HTML formatted string.
 */
function formatBotReply(rawText) {
    if (!rawText || typeof rawText !== 'string') {
        return '';
    }

    let formattedText = rawText;

    // 1. Handle Code Blocks (must be done before other formatting to prevent issues)
    // Matches ```language\ncode\n``` or ```\ncode\n```
    formattedText = formattedText.replace(/```(\w*)\n([\s\S]+?)\n```/g, (match, lang, code) => {
        // Basic escaping for HTML entities within the code block
        const escapedCode = code.replace(/&/g, '&amp;')
                               .replace(/</g, '&lt;')
                               .replace(/>/g, '&gt;');
        // You could add syntax highlighting libraries here based on `lang`
        return `<pre><code${lang ? ` class="language-${lang}"` : ''}>${escapedCode}</code></pre>`;
    });

    // 2. Handle Paragraphs and Lists (split by lines to process more easily)
    const lines = formattedText.split('\n');
    let htmlOutput = [];
    let inList = false;

    for (let i = 0; i < lines.length; i++) {
        let line = lines[i].trim();

        // Check for empty lines to create new paragraphs
        if (line === '') {
            if (inList) {
                htmlOutput.push('</ul>');
                inList = false;
            }
            // Add a paragraph break, but avoid multiple empty paragraphs if there are consecutive empty lines
            if (htmlOutput.length > 0 && !htmlOutput[htmlOutput.length - 1].endsWith('</p>')) {
                 htmlOutput.push('<p></p>'); // Add an empty paragraph for spacing
            }
            continue;
        }

        // Check for List Items
        if (line.startsWith('* ') || line.startsWith('- ')) {
            if (!inList) {
                htmlOutput.push('<ul>');
                inList = true;
            }
            // Remove the bullet point and trim again
            let listItemContent = line.substring(2).trim();
            htmlOutput.push(`<li>${listItemContent}</li>`);
        } else {
            // If we were in a list, close it
            if (inList) {
                htmlOutput.push('</ul>');
                inList = false;
            }
            // Treat as a regular paragraph line (will be wrapped in <p> later if not a direct HTML element)
            htmlOutput.push(line);
        }
    }

    // Close any open list at the end
    if (inList) {
        htmlOutput.push('</ul>');
    }

    // Join lines and then apply inline formatting and final paragraph wrapping
    let finalContent = htmlOutput.join('\n');

    // 3. Handle Inline Code
    formattedText = finalContent.replace(/`([^`]+)`/g, '<code>$1</code>');

    // 4. Handle Bold (stronger emphasis)
    formattedText = formattedText.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // 5. Handle Italics (lighter emphasis)
    // This regex ensures it doesn't match if it's already part of a **bold** match
    formattedText = formattedText.replace(/(?<!\*)\*(?!\*)(.*?)(?<!\*)\*(?!\*)/g, '<em>$1</em>'); // Matches *text* not preceded/followed by *
    formattedText = formattedText.replace(/_([^_]+)_/g, '<em>$1</em>'); // Matches _text_

    // 6. Wrap remaining plain text lines in paragraphs
    // This is a bit tricky after list processing. A common approach is to
    // split by newlines again and wrap anything that isn't already HTML.
    // For simplicity, let's assume if it's not starting with an HTML tag it's a paragraph.
    const finalLines = formattedText.split('\n');
    let outputWithParagraphs = [];
    let currentParagraph = [];

    for (const line of finalLines) {
        const trimmedLine = line.trim();
        // Check if the line looks like an HTML tag, or if it's empty (already handled for new paragraphs)
        if (trimmedLine === '' || trimmedLine.startsWith('<') || trimmedLine.startsWith('</')) {
            if (currentParagraph.length > 0) {
                outputWithParagraphs.push(`<p>${currentParagraph.join(' ')}</p>`);
                currentParagraph = [];
            }
            outputWithParagraphs.push(line); // Add the HTML tag or empty line directly
        } else {
            currentParagraph.push(line); // Collect lines for the current paragraph
        }
    }
    // Add any remaining paragraph content
    if (currentParagraph.length > 0) {
        outputWithParagraphs.push(`<p>${currentParagraph.join(' ')}</p>`);
    }


    return outputWithParagraphs.join('\n').trim();
}
