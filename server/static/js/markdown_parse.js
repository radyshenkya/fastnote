function markdown_parse() {
    let markdown_els = document.getElementsByClassName("markdown-parse");
    const converter = new showdown.Converter({
        "emoji": true, "tables": true,
        "simplifiedAutoLink": true,
        "strikethrough": true,
        "underline": true,
    });

    for (let index = 0; index < markdown_els.length; index++) {
        const element = markdown_els[index];
        const text = element.innerHTML;
        element.innerHTML = converter.makeHtml(text);
    }
}

markdown_parse();