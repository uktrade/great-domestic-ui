import * as annotator from 'annotator';

import './annotator.css';

export interface Annotation {
    contentPath: string,
    annotation: any,
    highlights: any[],
    onDelete(),
}

// trim strips whitespace from either end of a string.
//
// This usually exists in native code, but not in IE8.
function trim(s: string): string {
    if (typeof String.prototype.trim === 'function') {
        return String.prototype.trim.call(s);
    } else {
        return s.replace(/^[\s\xA0]+|[\s\xA0]+$/g, '');
    }
}

// annotationFactory returns a function that can be used to construct an
// annotation from a list of selected ranges.
function annotationFactory(contextEl, ignoreSelector) {
    return function (ranges) {
        var text = [],
            serializedRanges = [];

        for (var i = 0, len = ranges.length; i < len; i++) {
            var r = ranges[i];
            text.push(trim(r.text()));
            serializedRanges.push(r.serialize(contextEl, ignoreSelector));
        }

        return {
            quote: text.join(' / '),
            ranges: serializedRanges
        };
    };
}

export class AnnotatableSection {
    contentPath: string;
    element: HTMLElement;
    highlighter: any;
    makeAnnotation: any;
    adder: any;
    selector: any;

    constructor(contentPath, element, onNewComment) {
        this.contentPath = contentPath;
        this.element = element;

        this.highlighter = new annotator.ui.highlighter.Highlighter(element);
        this.makeAnnotation = annotationFactory(element, '.annotator-hl');
        this.adder = new annotator.ui.adder.Adder({
            onCreate: annotation => {
                let highlights = this.highlighter.draw(annotation);
                let onDelete = () => {
                    this.highlighter.undraw(annotation);
                }

                onNewComment({contentPath, annotation, highlights, onDelete});
            }
        });
        this.adder.attach();

        this.selector = new annotator.ui.textselector.TextSelector(element, {
            onSelection: (ranges, event) => {
                if (ranges.length > 0) {
                    let annotation = this.makeAnnotation(ranges);
                    let interactionPoint = annotator.util.mousePosition(event);
                    this.adder.load(annotation, interactionPoint);
                } else {
                    this.adder.hide();
                }
            }
        });
    }

    addAnnotation(annotationInfo): Annotation {
        let highlights = this.highlighter.draw(annotationInfo);

        let onDelete = () => {
            this.highlighter.undraw(annotationInfo);
        }

        return {contentPath: this.contentPath, annotation: annotationInfo, highlights, onDelete};
    }
}
