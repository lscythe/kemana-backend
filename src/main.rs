const SERVICE_NAME: &str = "kemana-backend";

fn banner() -> String {
    format!("{SERVICE_NAME} {}", env!("CARGO_PKG_VERSION"))
}

fn main() {
    println!("{}", banner());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn banner_names_the_service_and_its_version() {
        assert_eq!(
            banner(),
            format!("kemana-backend {}", env!("CARGO_PKG_VERSION"))
        );
    }
}
