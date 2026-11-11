//! Greetings: the smallest crate that passes every check in the kit.
#![forbid(unsafe_code)]

/// The most times [`cheer`] repeats a greeting. A number with a name: the
/// reader learns what it means, and changing it changes it everywhere.
pub const MAX_CHEERS: usize = 3;

/// Who is greeted when nobody is named.
pub const NOBODY: &str = "world";

/// Greets `name`.
#[must_use]
pub fn greet(name: &str) -> String {
    format!("Hello, {name}!")
}

/// Greets `name` `times` times, but never more than [`MAX_CHEERS`].
#[must_use]
pub fn cheer(name: &str, times: usize) -> Vec<String> {
    (0..times.min(MAX_CHEERS)).map(|_| greet(name)).collect()
}

/// The greeting for a program's arguments: the first one after the
/// program's own name, or [`NOBODY`].
#[must_use]
pub fn greeting_for(mut args: impl Iterator<Item = String>) -> String {
    let name = args.nth(1).unwrap_or_else(|| NOBODY.to_owned());
    greet(&name)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn greets_by_name() {
        assert_eq!(greet("Ada"), "Hello, Ada!");
    }

    #[test]
    fn cheers_no_more_than_the_limit() {
        assert_eq!(cheer("Ada", 10).len(), MAX_CHEERS);
        assert!(cheer("Ada", 0).is_empty());
    }

    #[test]
    fn greets_the_first_argument_or_the_world() {
        let args = |list: &[&str]| list.iter().map(|s| (*s).to_owned()).collect::<Vec<_>>();
        assert_eq!(
            greeting_for(args(&["hello", "Ada"]).into_iter()),
            "Hello, Ada!"
        );
        assert_eq!(greeting_for(args(&["hello"]).into_iter()), "Hello, world!");
    }
}
