import Adw from 'gi://Adw';
import Gio from 'gi://Gio';
import GLib from 'gi://GLib';
import GObject from 'gi://GObject';
import Gtk from 'gi://Gtk?version=4.0';

export class Window extends Adw.ApplicationWindow {
    private _toastOverlay!: Adw.ToastOverlay;

    static {
        GObject.registerClass(
            {
                Template:
                    'resource:///org/example/TypescriptTemplate/window.ui',
                InternalChildren: ['toastOverlay'],
            },
            this
        );
    }

    constructor(params?: Partial<Adw.ApplicationWindow.ConstructorProperties>) {
        super(params);

        const openLink = new Gio.SimpleAction({
            name: 'open-link',
            parameter_type: GLib.VariantType.new('s'),
        });

        openLink.connect('activate', (_source, param) => {
            if (param) {
                const link = param.get_string()[0];

                const launcher = new Gtk.UriLauncher({ uri: link });

                /* eslint-disable @typescript-eslint/no-unsafe-call */
                /* eslint-disable @typescript-eslint/no-unsafe-member-access */
                launcher
                    .launch(this, null)
                    // @ts-expect-error GtkUriLauncher.launch isn't properly generated in our type defs
                    .then(() => {
                        const toast = new Adw.Toast({
                            title: _('Opened link'),
                        });
                        this._toastOverlay.add_toast(toast);
                    })
                    .catch(console.error);
            }
        });

        this.add_action(openLink);
    }
}
