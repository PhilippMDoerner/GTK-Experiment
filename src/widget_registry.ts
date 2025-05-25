import GObject from "gi://GObject";
import { TSWidget } from "./widget_meta";

const WIDGET_REGISTRY: TSWidget[] = [
];

export function load_widgets(){
    WIDGET_REGISTRY.forEach(widget => GObject.registerClass(
        {
            Template: widget.template,
            GTypeName: widget.GTypeName,
        },
        widget.klass,
    ))
}
