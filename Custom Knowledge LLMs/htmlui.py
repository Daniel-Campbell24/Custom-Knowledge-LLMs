css = '''
<style>
.chat-message {
    padding: 1.5rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex;
}

.chat-message.user {
    background-color: #5f9ea0; /* Your message color: Turquoise */
}

.chat-message.bot {
    background-color: #ffa07a; /* Robot message color: Salmon */
}

.chat-message .avatar {
    width: 20%;
}

.chat-message .avatar img {
    max-width: 78px;
    max-height: 78px;
    border-radius: 50%;
    object-fit: cover;
}

.chat-message .message {
    width: 80%;
    padding: 0 1.5rem;
    color: #fff;
}
</style>
'''


robot_image = '''
<div class="chat-message robot">
    <div class="avatar">
        <img src="https://i.ibb.co/qW9DHq6/Copy-of-DELTA-8.png" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

you_image = '''
<div class="chat-message you">
    <div class="avatar">
        <img src="https://i.ibb.co/HnDgnDZ/UTOPIA-47.png">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''