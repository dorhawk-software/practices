//! Prints a greeting for the name given, or for the world.
#![forbid(unsafe_code)]

fn main() {
    println!("{}", hello::greeting_for(std::env::args()));
}
