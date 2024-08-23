mod files;

use clap::{Parser, Subcommand};
use std::fs;
use std::process;
use files::structure::run_tree_command;

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    #[command(subcommand)]
    command: Command,
}

#[derive(Subcommand, Debug)]
enum Command {
    Modify {
        /// Input file name
        file: String,

        /// Config file name
        #[arg(long, default_value = "config.toml")]
        config: String,
    },
    Restore {
        /// Input file name
        file: String,

        /// Backup file name
        #[arg(long)]
        backup: Option<String>,
    },
}

fn main() {
    let args = Args::parse();

    match args.command {
        Command::Modify { file, config } => {
            println!("Modifying file: {}", file);
            println!("Using config file: {}", config);

            // Read the content of the files
            let file_content = match fs::read_to_string(&file) {
                Ok(content) => content,
                Err(e) => {
                    eprintln!("Error reading file {}: {}", file, e);
                    process::exit(1);
                }
            };

            let config_content = match fs::read_to_string(&config) {
                Ok(content) => content,
                Err(e) => {
                    eprintln!("Error reading config file {}: {}", config, e);
                    process::exit(1);
                }
            };

            let decoded: toml::Value = match toml::from_str(&config_content) {
                Ok(value) => value,
                Err(e) => {
                    eprintln!("Error parsing config file: {}", e);
                    process::exit(1);
                }
            };

            println!("Decoded config:\n{:#?}", decoded);

            let mut ignore_vec: Vec<&str> = Vec::new();

            if let Some(tree) = decoded.get("tree").and_then(|v| v.as_table()) {
                // Access the "ignore" array within the "tree" table
                if let Some(ignore) = tree.get("ignore").and_then(|v| v.as_array()) {

                    ignore.iter().for_each(|value| {
                        if let Some(s) = value.as_str() {
                            println!("Ignored item: {}", s);
                            ignore_vec.push(s);
                        }
                    });
                    // for value in ignore {
                    //     if let Some(s) = value.as_str() {
                    //         println!("Ignored item: {}", s);
                    //     }
                    // }
                }
            }

            let ignore_list = Some(ignore_vec);

            println!("Ignore list: {:?}", ignore_list);

            match run_tree_command(ignore_list) {
                Ok(output) => println!("{}", output),
                Err(e) => eprintln!("Error running tree command: {}", e),
            }

            // let ignore_vec: Vec<&str> = match decoded.get("ignore") {
            //     Some(value) => match value.as_array() {
            //         Some(array) => array.iter().map(|v| v.as_str().unwrap()).collect(),
            //         None => {
            //             eprintln!("Ignore value must be an array");
            //             process::exit(1);
            //         }
            //     },
            //     None => {
            //         eprintln!("Ignore value is required in config file");
            //         process::exit(1);
            //     }
            // };

            // let ignore_list = Some(ignore_vec);

            // println!("Ignore list: {:?}", ignore_list);
        }
        Command::Restore { file, backup } => {
            println!("Restoring file: {}", file);
            match backup {
                Some(backup) => {
                    println!("Using backup file: {}", backup);

                    // Read the content of the files
                    let file_content = match fs::read_to_string(&file) {
                        Ok(content) => content,
                        Err(e) => {
                            eprintln!("Error reading file {}: {}", file, e);
                            process::exit(1);
                        }
                    };

                    let backup_content = match fs::read_to_string(&backup) {
                        Ok(content) => content,
                        Err(e) => {
                            eprintln!("Error reading backup file {}: {}", backup, e);
                            process::exit(1);
                        }
                    };

                    // Here you would typically restore the file content based on the backup
                    // For this example, we'll just print the contents
                    println!("File content:\n{}", file_content);
                    println!("Backup content:\n{}", backup_content);
                }
                None => {
                    eprintln!("Backup file is required for restore command");
                    process::exit(1);
                }
            }
        }
    }
}
