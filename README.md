# Sublime Text Gleam 💫

A Sublime text language package for the [Gleam](https://gleam.run) programming language.

### Features

- 🎨 Gleam syntax highlighting.
- 👔 Gleam format on save.

![highlighting demo](https://github.com/itsgreggreg/sublime-text-gleam/blob/main/images/highlighting_demo.jpg?raw=true)

## Installation

For formatting to work you must have `gleam` installed on your computer.
Follow these instructions for installing `gleam`: https://gleam.run/getting-started/

You can get this package on [Package Control](http://packagecontrol.io).

1. Open up Sublime text
2. Press `CTRL + Shift + P` inside Sublime Text
3. Type `Gleam` and press enter.

Otherwise, go to your `Packages` folder, and execute

```bash
git clone git@github.com:itsgreggreg/sublime-text-gleam.git Gleam
```

## Settings

To access setings for this package click on:

`Preferences -> Package Settings -> Gleam -> Settings`

### Format on Save

`format_on_save` is on for all gleam files by default, you can change this
by opening the package settings and changing `format_on_save` to one of the
available options.

For the full list of options open up the settings for this package.

### Gleam executable absolute path

This package will try to find `gleam` automatically in your system but in case
it can't or you want to use a specific version of `gleam`, change the
`absolute_path` option in your settings file to be the location of the `gleam`
executable on your computer.

If you know `gleam` is installed but formatting is not working, try running
`which gleam` in the terminal and pasting the output of that command into
`absolute_path`.

## Contributions

Welcome! Feel free to file a bug or make a pull request.
