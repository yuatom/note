# Could not link phinze/cask manpages

# try this first
brew untap caskroom/homebrew-cask
brew untap phinze/homebrew-cask
# otherwise just run this
rm -rf $(brew --prefix)/Library/Taps/phinze-cask
rm $(brew --prefix)/Library/Formula/brew-cask.rb
rm -rf $(brew --prefix)/Library/Taps/caskroom
# and to finish up
brew uninstall --force brew-cask
brew update; brew cleanup; brew cask cleanup

