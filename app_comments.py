from flask import session, render_template, redirect, request
from db import db
from werkzeug.security import check_password_hash, generate_password_hash
import secrets
from datetime import datetime, timezone

def send_comment(username, list_name, content, visible):
    sent_at = datetime.now(timezone.utc)
    sql = "INSERT INTO message (username, list_name, content, visible, sent_at) VALUES (:username, :list_name, :content, :visible, :sent_at)"
    db.session.execute(sql, {"username":username, "list_name":list_name, "content":content, "visible":visible, "sent_at":sent_at})
    db.session.commit()
    return True

def hide_comment(comment_id, visible):
    sql = "UPDATE message SET visible=0 WHERE id=:comment_id;"
    db.session.execute(sql, {"comment_id":comment_id})
    db.session.commit()
    return True
