import * as React from 'react';
import { Comment, CommentReply } from '../../state';
import APIClient from '../../api';
import { updateReply, deleteReply } from '../../actions';

import './style.scss';

export interface CommentReplyProps {
    comment: Comment;
    reply: CommentReply;
    store: any;
    api: APIClient;
}

class CommentReplyHeader extends React.Component<CommentReplyProps> {
    render() {
        return <div className="comment-reply__header">
            <hr/>
            <div className="comment-reply__header-info">
                <h2>Author</h2>
                <p className="comment-reply__date">10:25 May 10</p>
            </div>
            <div className="comment-reply__header-actions">
                {this.props.children}
            </div>
        </div>;
    }
}

export default class CommentReplyComponent extends React.Component<CommentReplyProps> {

    renderEditing() {
        let { comment, reply, store, api } = this.props;

        let onChangeText = e => {
            e.preventDefault();

            store.dispatch(updateReply(comment.localId, reply.localId, {
                text: e.target.value,
            }));
        };

        let onSave = async e => {
            e.preventDefault();

            store.dispatch(updateReply(comment.localId, reply.localId, {
                mode: 'saving',
            }));

            await api.saveCommentReply(comment, reply);

            store.dispatch(updateReply(comment.localId, reply.localId, {
                mode: 'default',
            }));
        };

        let onCancel = e => {
            e.preventDefault();

            comment.annotation.onDelete();
            store.dispatch(updateReply(comment.localId, reply.localId, {
                mode: 'default',
                text: comment.editPreviousText,
            }));
        };

        return <>
            <CommentReplyHeader {...this.props}>
                <button onClick={onSave}>Save</button>
                <button onClick={onCancel}>Cancel</button>
            </CommentReplyHeader>
            <textarea className="comment-reply__input" value={reply.text} onChange={onChangeText} style={{resize: 'none'}} />
        </>;
    }

    renderSaving() {
        let { reply } = this.props;

        return <>
            <CommentReplyHeader {...this.props}>
                <p>Saving...</p>
            </CommentReplyHeader>
            <textarea className="comment-reply__input" value={reply.text} style={{resize: 'none'}} />
        </>;
    }

    renderDeleting() {
        let { reply } = this.props;

        return <>
            <CommentReplyHeader {...this.props}>
                <p>Deleting...</p>
            </CommentReplyHeader>
            <p className="comment-reply__text">{reply.text}</p>
        </>;
    }

    renderDefault() {
        let { comment, reply, store, api } = this.props;

        let onClickEdit = async e => {
            e.preventDefault();

            store.dispatch(updateReply(comment.localId, reply.localId, {
                mode: 'editing',
                editPreviousText: reply.text,
            }));
        };

        let onClickDelete = async e => {
            e.preventDefault();

            store.dispatch(updateReply(comment.localId, reply.localId, {
                mode: 'deleting',
            }));

            await api.deleteCommentReply(comment, reply);

            store.dispatch(deleteReply(comment.localId, reply.localId));
        };

        return <>
            <CommentReplyHeader {...this.props}>
                <a href="#" onClick={onClickEdit}>Edit</a>
                <a href="#" onClick={onClickDelete}>Delete</a>
            </CommentReplyHeader>
            <p className="comment-reply__text">{reply.text}</p>
        </>;
    }

    render() {
        let inner;

        switch (this.props.reply.mode) {
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

        return <li key={this.props.reply.localId} className="comment-reply" data-reply-id={this.props.reply.localId}>
            {inner}
        </li>;
    }
}
