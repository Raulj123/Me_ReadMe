{
  description = "A Nix-flake-based Python development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/release-23.11";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
   
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = import nixpkgs {inherit system;};
    in {
      devShells.default = pkgs.mkShell {
        packages = with pkgs;
          [
            # Python development
            python311
            virtualenv
          ]
          ++ (with pkgs.python311Packages; [
            pip
            PyGithub
            python-dotenv
          ]);

        shellHook = ''
          ${pkgs.python311}/bin/python --version
        '';
      };
    });
}