// A small picture of a window, as a GPUI app's Settings pane drew it: the
// sidebar's square corners showed past the picture's rounded ones.
fn picture(side: Rgba) -> Div {
    div()
        .relative()
        .w(px(64.))
        .h(px(44.))
        .rounded(px(7.))
        .overflow_hidden()
        .border_1()
        .child(
            div()
                .absolute()
                .left_0()
                .top_0()
                .bottom_0()
                .w(px(20.))
                .bg(side),
        )
}

fn pill() -> Div {
    div().rounded_full().overflow_x_hidden().child(div().size_full())
}

fn card(on: bool) -> Div {
    div()
        .when(on, |d| d.rounded(px(4.)))
        .overflow_y_hidden()
}

fn sheet(on: bool) -> Div {
    div()
        .overflow_hidden()
        .when(on, |this| {
            this.rounded_t(px(6.))
        })
}

fn row() -> Div {
    div()
        .rounded(px(10.))
        // practices-allow clip: swipe
        .overflow_hidden()
}
