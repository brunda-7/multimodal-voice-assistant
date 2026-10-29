from django.shortcuts import render
from django.http import JsonResponse
from .models import Conversation

from django.shortcuts import render
from django.http import JsonResponse
from .models import Conversation

def chat_interface(request):
    # Get or create conversation with better session handling
    conversation_id = request.session.get('conversation_id')
    
    print(f"🎯 Session conversation_id: {conversation_id}")
    
    if conversation_id:
        try:
            conversation = Conversation.objects.get(id=conversation_id)
            print(f"✅ Found existing conversation: {conversation.id}")
        except Conversation.DoesNotExist:
            conversation = Conversation.objects.create(title="New Conversation")
            request.session['conversation_id'] = conversation.id
            request.session.modified = True  # Force session save
            print(f"🆕 Created new conversation: {conversation.id}")
    else:
        conversation = Conversation.objects.create(title="New Conversation")
        request.session['conversation_id'] = conversation.id
        request.session.modified = True  # Force session save
        print(f"🆕 Created first conversation: {conversation.id}")
    
    context = {
        'conversation_id': conversation.id,
    }
    return render(request, 'chat/index.html', context)