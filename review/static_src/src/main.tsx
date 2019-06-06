import * as React from 'react';
import * as ReactDOM from 'react-dom';
import {createStore} from 'redux';

import APIClient from './api';
import {Annotation, AnnotatableSection} from './utils/annotation';
import {LayoutController} from './utils/layout';
import {getNextCommentId, getNextReplyId} from './utils/sequences';
import {Comment, CommentReply, reducer} from './state';
import {addComment, addReply, setFocusedComment} from './actions';
import CommentComponent from './components/Comment';

import './main.scss';

function Comments(props: {store, api: APIClient, layout: LayoutController, comments: Comment[]}) {
    let commentsRendered = props.comments.map(comment => <CommentComponent key={comment.localId} store={props.store} api={props.api} layout={props.layout} comment={comment} />);

    return <ol>
        {commentsRendered}
    </ol>;
}

function initCommentsApp(element: HTMLElement, api: APIClient, addAnnotatableSections: (addAnnotatableSection: (contentPath: string, element: HTMLElement) => void) => void) {
    let annotatableSections: {[contentPath: string]: AnnotatableSection} = {};
    let focusedComment = null;

    let store = createStore(reducer);
    let layout = new LayoutController();

    store.subscribe(() => {
        let state = store.getState();
        let commentList: Comment[] = [];

        for (let commentId in state.comments) {
            commentList.push(state.comments[commentId]);
        }

        // Check if the focused comment has changed
        if (state.focusedComment != focusedComment) {
            // Tell layout controller about the focused comment
            // so it is moved alongside it's annotation
            layout.setFocusedComment(state.focusedComment);

            // Unfocus previously focused annotation
            if (focusedComment) {
                // Note: the comment may have just been deleted. In that case,
                // don't worry about unfocusing the annotation as that will be
                // deleted
                if (focusedComment in state.comments) {
                    state.comments[focusedComment].annotation.onUnfocus();
                }
            }

            // Focus the new focused annotation
            if (state.focusedComment) {
                state.comments[state.focusedComment].annotation.onFocus();
            }

            focusedComment = state.focusedComment;
        }

        ReactDOM.render(<Comments store={store} api={api} layout={layout} comments={commentList} />, element, () => {
            // Render again if layout has changed (eg, a comment was added, deleted or resized)
            // This will just update the "top" style attributes in the comments to get them to move
            if (layout.isDirty) {
                layout.refresh();

                ReactDOM.render(<Comments store={store} api={api} layout={layout} comments={commentList} />, element);
            }
        });
    });

    let newComment = (annotation: Annotation) => {
        let commentId = getNextCommentId();

        // Focus comment when annotation is clicked
        annotation.setOnClickHandler(() => {
            store.dispatch(setFocusedComment(commentId));
        });

        // Let layout engine know the annotation so it would position the comment correctly
        layout.setCommentAnnotation(commentId, annotation)

        // Create the comment
        store.dispatch(addComment(Comment.makeNew(commentId, annotation)));

        // Focus the comment
        store.dispatch(setFocusedComment(commentId));
    };

    addAnnotatableSections((contentPath, element) => {
        annotatableSections[contentPath] = new AnnotatableSection(contentPath, element, newComment);
    });

    // Fetch existing comments
    api.fetchAllComments().then(comments => {
        for (let comment of comments) {
            let section = annotatableSections[comment.content_path];
            if (!section) {
                continue
            }

            // Create annotation
            let annotation = section.addAnnotation({
                quote: comment.quote,
                ranges: [{
                    start: comment.start_xpath,
                    startOffset: comment.start_offset,
                    end: comment.end_xpath,
                    endOffset: comment.end_offset,
                }]
            });

            let commentId = getNextCommentId();

            // Focus comment when annotation is clicked
            annotation.setOnClickHandler(() => {
                store.dispatch(setFocusedComment(commentId));
            });

            // Let layout engine know the annotation so it would position the comment correctly
            layout.setCommentAnnotation(commentId, annotation);

            // Create comment
            store.dispatch(addComment(Comment.fromApi(commentId, annotation, comment)));

            // Create replies
            for (let reply of comment.replies) {
                store.dispatch(addReply(commentId, CommentReply.fromApi(getNextReplyId(), reply)));
            }
        }
    });
}

window['CommentsAPI'] = APIClient;
window['initCommentsApp'] = initCommentsApp;
