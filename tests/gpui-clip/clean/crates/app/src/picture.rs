// The same picture, drawn right: the sidebar rounds the corners it fills
// with the picture's radius minus its border (7 - 1), and nothing clips.
// Text here never counts: .rounded(px(7.)).overflow_hidden()
/* Nor in a block comment: .rounded(px(7.)).overflow_hidden() /* nested */ */
fn picture(side: Rgba) -> Div {
    div()
        .relative()
        .w(px(64.))
        .h(px(44.))
        .rounded(px(7.))
        .border_1()
        .child(
            div()
                .absolute()
                .left_0()
                .top_0()
                .bottom_0()
                .w(px(20.))
                .rounded_l(px(6.))
                .bg(side),
        )
}

// The parent rounds, its child clips: two elements.
fn label(name: &str) -> Div {
    div()
        .rounded(px(7.))
        .p(px(8.))
        .child(div().overflow_hidden().text_ellipsis().child(name.to_owned()))
}

// The parent clips, its children round: two elements again.
fn list(items: Vec<String>) -> Div {
    div()
        .overflow_hidden()
        .children(items.into_iter().map(|item| div().rounded(px(4.)).child(item)))
        .child(div().rounded_full())
}

// Separate statements build separate elements.
fn two() -> (Div, Div) {
    let a = div().rounded(px(3.));
    let b = div().overflow_hidden();
    (a, b)
}

// No radius at all.
fn square() -> Div {
    div().rounded_none().overflow_hidden()
}

// Strings and characters that look like code, and lifetimes.
fn words<'a>(s: &'a str) -> (&'a str, char, char, &'static str) {
    let _ = ".rounded(px(7.)).overflow_hidden()";
    let _ = r#"div().rounded(px(2.)).overflow_hidden() "quoted" "#;
    (s, '(', ')', "\".rounded(px(1.)).overflow_hidden()")
}

// A clip kept on purpose, said so with its reason.
fn swipe_row(row: Div) -> Div {
    div()
        .rounded(px(10.))
        // practices-allow clip: the row slides out of it, and every child rounds its own corners
        .overflow_hidden()
        .child(row.rounded(px(10.)))
}

// A closure with two parameters is a handler, not the element.
fn button() -> Div {
    div()
        .overflow_hidden()
        .on_click(|_, cx| cx.rounded(px(3.)))
}
