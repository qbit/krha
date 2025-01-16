{ pkgs ? import <nixpkgs> { } }:
with pkgs;
let
  pythonEnv = python3.withPackages (
    p: with p; [
      dbus-python
      pygobject3
      requests
    ]
  );
in pkgs.mkShell {
  shellHook = ''
    PS1='\u@\h:\w; '
  '';
  buildInputs = with pkgs; [
    pythonEnv
    wrapGAppsHook
    gobject-introspection
  ];
}
