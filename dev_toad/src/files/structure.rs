use std::process::Command;

pub fn run_tree_command(ignore_list: Option<Vec<&str>>) -> Result<String, std::io::Error> {
    // let output = Command::new("tree").args(["-I", "target"]).output()?;

    let output = match ignore_list {
        Some(list) => {
            let mut args = vec!["-I".to_string()];
            args.push(list.join(","));
            Command::new("tree").args(args).output()?
        }
        None => Command::new("tree").output()?,
    };

    if output.status.success() {
        Ok(String::from_utf8_lossy(&output.stdout).into_owned())
    } else {
        Err(std::io::Error::new(
            std::io::ErrorKind::Other,
            format!(
                "Command failed with error: {}",
                String::from_utf8_lossy(&output.stderr)
            ),
        ))
    }
}
