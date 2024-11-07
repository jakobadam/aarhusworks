#!/bin/bash
# This script processes a markdown file to add rendered SVGs of mermaid diagram blocks.
# Usage: ./mermaid2svg.sh <file>

# TODO Consider also adding <style>pre:has(.language-mermaid) { display: none;}</style>
file=$1

if [ -z "$file" ]; then
    echo "No file provided. Usage: $0 <file>"
    exit 1
fi

process_mermaid_block() {
    local block_content="$1"
    local svg_file="temp.svg"

    echo "$block_content" | mmdc -q -i - -o "$svg_file"
    echo '<div class="mermaid-svg" style="text-align:center">'
    cat "${svg_file}"
    echo "</div><!--mermaid-svg-end-->"
}

post_content=$(cat "${file}")

updated_content=""

while [[ "$post_content" =~ (.*)(\`\`\`mermaid)([^\`]+)(\`\`\`)(.*</div><!--mermaid-svg-end-->)?(.*) ]]; do
    pre_content="${BASH_REMATCH[1]}"
    mermaid_block="${BASH_REMATCH[3]}"
    post_content="${BASH_REMATCH[6]}"

    svg_content=$(process_mermaid_block "$mermaid_block")

    updated_content+="${pre_content}\`\`\`mermaid${mermaid_block}\`\`\`\n${svg_content}"
done

updated_content+="$post_content"

echo "${updated_content}" > "${file}"
