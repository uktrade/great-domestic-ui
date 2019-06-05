import * as React from 'react';
import * as ReactDOM from 'react-dom';

import {Comment} from '../state';
import {updateComment, deleteComment} from '../actions';
import APIClient from '../api';
import {LayoutController} from '../utils/layout';

export interface CommentProps {
    store: any,
    comment: Comment,
    api: APIClient,
    layout: LayoutController,
}

export default class CommentComponent extends React.Component<CommentProps> {
    renderCreating() {
        let { comment, store, api } = this.props;

        let onChangeText = e => {
            e.preventDefault();

            store.dispatch(updateComment(comment.localId, {
                text: e.target.value,
            }));
        };

        let onSave = async e => {
            e.preventDefault();

            store.dispatch(updateComment(comment.localId, {
                mode: 'saving',
            }));

            let commentData = await api.saveComment(comment);

            store.dispatch(updateComment(comment.localId, {
                mode: 'default',
                remoteId: commentData.id,
            }));
        };

        let onCancel = e => {
            e.preventDefault();

            comment.annotation.onDelete();
            store.dispatch(deleteComment(comment.localId));
        };

        return <>
            <textarea value={comment.text} onChange={onChangeText} />
            <button onClick={onSave}>Add Comment</button>
            <button onClick={onCancel}>Cancel</button>
        </>;
    }

    renderEditing() {
        let { comment, store } = this.props;

        let onChangeText = e => {
            e.preventDefault();

            store.dispatch(updateComment(comment.localId, {
                text: e.target.value,
            }));
        };

        let onSave = e => {
            e.preventDefault();

            store.dispatch(updateComment(comment.localId, {
                mode: 'default',
            }));
        };

        let onCancel = e => {
            e.preventDefault();

            comment.annotation.onDelete();
            store.dispatch(updateComment(comment.localId, {
                mode: 'default',
                text: e.target.value,  // TODO: Restore previous content
            }));
        };

        return <>
            <textarea  value={comment.text} onChange={onChangeText} />
            <button onClick={onSave}>Save</button>
            <button onClick={onCancel}>Cancel</button>
        </>;
    }

    renderSaving() {
        let { comment } = this.props;

        return <>
            <p>{comment.text}</p>
            <p>Saving...</p>
        </>;
    }

    renderDeleting() {
        let { comment } = this.props;

        return <>
            <p>{comment.text}</p>
            <p>Deleting...</p>
        </>;
    }

    renderDefault() {
        let { comment, store, api } = this.props;

        let onClickDelete = async e => {
            e.preventDefault();

            store.dispatch(updateComment(comment.localId, {
                mode: 'deleting',
            }));

            await api.deleteComment(comment);

            store.dispatch(deleteComment(comment.localId));
            comment.annotation.onDelete();
        }

        return <>
            <div>
                <h2>{comment.author}</h2>
                <p>DATE</p>
            </div>
            <p>{comment.text}</p>
            <a href="#" onClick={onClickDelete}>Delete</a>
            <ul>
                REPLIES
            </ul>
            <textarea placeholder="Reply" />
            <button>Send Reply</button>
            <button>Cancel</button>
        </>
    }

    render() {
        let inner;

        switch (this.props.comment.mode) {
            case 'creating':
                inner = this.renderCreating();
                break;

            case 'editing':
                inner = this.renderEditing();
                break;

            case 'saving':
                inner = this.renderSaving();
                break;

            case 'deleting':
                inner = this.renderDeleting();
                break;

            default:
                inner = this.renderDefault();
                break;
        }

        let position = this.props.layout.getCommentPosition(this.props.comment.localId);
        return <li key={this.props.comment.localId} className="comment" style={{position: 'absolute', top: `${position}px`}} data-comment-id={this.props.comment.localId}>
            {inner}
        </li>;
    }

    componentDidMount() {
        let element = ReactDOM.findDOMNode(this);

        if (element instanceof HTMLElement) {
            // If this is a new comment, focus in the edit box
            if (this.props.comment.mode == 'creating') {
                element.querySelector('textarea').focus();
            }

            this.props.layout.setCommentElement(this.props.comment.localId, element);
            this.props.layout.setCommentHeight(this.props.comment.localId, element.offsetHeight);
        }
    }

    componentWillUnmount() {
        this.props.layout.setCommentElement(this.props.comment.localId, null);
    }

    componentDidUpdate() {
        let element = ReactDOM.findDOMNode(this);

        // Keep height up to date so that other comments will be moved out of the way
        if (element instanceof HTMLElement) {
            this.props.layout.setCommentHeight(this.props.comment.localId, element.offsetHeight);
        }
    }
}
