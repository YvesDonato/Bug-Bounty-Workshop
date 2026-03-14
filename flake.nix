{
  description = "Direnv-backed Nix flake for the Bug Bounty Workshop Django app";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";
  };

  outputs = { self, nixpkgs }:
    let
      lib = nixpkgs.lib;
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];
      forAllSystems = lib.genAttrs systems;
      perSystem = system:
        let
          pkgs = import nixpkgs { inherit system; };
          pythonEnv = pkgs.python312.withPackages (ps: with ps; [
            django
            pillow
          ]);
          cleanSrc = pkgs.lib.cleanSourceWith {
            src = ./.;
            filter = path: type:
              let
                name = builtins.baseNameOf (toString path);
              in
                !(lib.elem name [
                  ".direnv"
                  ".git"
                  ".venv"
                  "__pycache__"
                  "db.sqlite3"
                  "media"
                  "result"
                  "venv"
                ]);
          };
          launcher = pkgs.writeShellApplication {
            name = "halftone-manage";
            runtimeInputs = [ pythonEnv ];
            text = ''
              export DJANGO_SETTINGS_MODULE="halftone_project.settings"
              export PYTHONDONTWRITEBYTECODE=1

              workdir="''${HALFTONE_WORKDIR:-$PWD}"

              if [ ! -f "$workdir/manage.py" ]; then
                echo "halftone-manage must be run from the repository root or with HALFTONE_WORKDIR pointing at it." >&2
                exit 1
              fi

              cd "$workdir"
              exec python manage.py "$@"
            '';
          };
        in
        {
          packages.default = launcher;

          apps.default = {
            type = "app";
            program = "${launcher}/bin/halftone-manage";
            meta = {
              description = "Django management command launcher for the Bug Bounty Workshop app";
            };
          };

          devShells.default = pkgs.mkShell {
            packages = [ pythonEnv ];

            env = {
              DJANGO_SETTINGS_MODULE = "halftone_project.settings";
              PYTHONDONTWRITEBYTECODE = "1";
            };

            shellHook = ''
              echo "Django Nix shell ready."
              echo "Run: python manage.py migrate"
              echo "Then: python manage.py runserver"
            '';
          };

          checks = {
            python-imports = pkgs.runCommand "python-imports" {
              nativeBuildInputs = [ pythonEnv ];
            } ''
              export HOME="$TMPDIR"
              python - <<'PY'
              import django
              import PIL

              print("Django", django.get_version())
              print("Pillow", PIL.__version__)
              PY

              touch "$out"
            '';

            django-check = pkgs.runCommand "django-check" {
              nativeBuildInputs = [ pythonEnv ];
            } ''
              export HOME="$TMPDIR"
              export DJANGO_SETTINGS_MODULE="halftone_project.settings"
              export PYTHONDONTWRITEBYTECODE=1

              cd ${cleanSrc}
              python manage.py check

              touch "$out"
            '';
          };
        };
    in
    {
      packages = forAllSystems (system: (perSystem system).packages);
      apps = forAllSystems (system: (perSystem system).apps);
      devShells = forAllSystems (system: (perSystem system).devShells);
      checks = forAllSystems (system: (perSystem system).checks);
    };
}
