import Gtk from "gi://Gtk";

export interface TSWidget {
    template: string;
    GTypeName: string;
    klass: new (...args: any[]) => Gtk.Widget
}
