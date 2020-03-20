# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from selenium import webdriver
import json
import os
from typing import Dict
import random
from typing import List, Union
from botbuilder.core import ActivityHandler, TurnContext, CardFactory
from botbuilder.schema import ChannelAccount, Attachment, Activity, ActivityTypes
from botbuilder.schema import (
    ConversationReference,
    ActionTypes,
    Attachment,
    ThumbnailCard,
    MediaUrl,
    CardAction,
    CardImage,
    ThumbnailUrl,
    Fact,
    ReceiptItem,
    AttachmentLayoutTypes,
    InputHints
)
def attachment_activity(
    attachment_layout: AttachmentLayoutTypes,
    attachments: List[Attachment],
    text: str = None,
    speak: str = None,
    input_hint: Union[InputHints, str] = InputHints.accepting_input,
) -> Activity:
    message = Activity(
        type=ActivityTypes.message,
        attachment_layout=attachment_layout,
        attachments=attachments,
        input_hint=input_hint,
    )
    if text:
        message.text = text
    if speak:
        message.speak = speak
    return message
import requests
# def get_api():
#     API_ENDPOINT_all = "https://corona.lmao.ninja/all"
#     API_ENDPOINT_country = 'https://corona.lmao.ninja/countries'
#     # sending post request and saving response as response object 
#     global_statistic = requests.get(url = API_ENDPOINT_all).json()
#     global_statistic['being_infected']=global_statistic['cases']-global_statistic['deaths']-global_statistic['recovered']
#     vietnam_statistic = [a for a in requests.get(url = API_ENDPOINT_country).json() if a['country']=='Vietnam'][0]
#     vietnam_statistic={key:vietnam_statistic[key] for key in ['cases','deaths','recovered']}
#     vietnam_statistic['being_infected']=vietnam_statistic['cases']-vietnam_statistic['deaths']-vietnam_statistic['recovered']
#     return {'global':global_statistic,'vietnam':vietnam_statistic}

def get_api():
    GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
    CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.binary_location = GOOGLE_CHROME_PATH
    driver = webdriver.Chrome(execution_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
    # driver = webdriver.Chrome(executable_path="C:\chromedriver.exe")
    url = "http://ncov.moh.gov.vn"
    driver.get(url)
    driver.implicitly_wait(3)
    vietnam={}
    vietnam['cases']=int(driver.find_element_by_id('VN-01').text.replace('.',''))
    vietnam['deaths']=int(driver.find_element_by_id('VN-02').text.replace('.',''))
    vietnam['recovered']=int(driver.find_element_by_id('VN-04').text.replace('.',''))
    vietnam['infected']=vietnam['cases']-vietnam['deaths']-vietnam['recovered']

    global_={}
    global_['cases']=int(driver.find_element_by_id('QT-01').text.replace('.',''))
    global_['deaths']=int(driver.find_element_by_id('QT-02').text.replace('.',''))
    global_['recovered']=int(driver.find_element_by_id('QT-04').text.replace('.',''))
    global_['infected']=global_['cases']-global_['deaths']-global_['recovered']

    newest=driver.find_element_by_xpath("//*[@id=\"yui_patched_v3_11_0_1_1582618410030_3628\"]/div[2]/div/p["+str(vietnam['cases']-30)+"]/strong/span[3]").text
    newest="Bệnh nhân "+str(vietnam['cases'])+newest
    driver.close()
    return {'global':global_,'vietnam':vietnam,'newest':newest}

def generate_reply(response_type):
    if response_type=='reply':
        text='My pleasure. Here some information: '
    elif response_type=='report':
        text='For your information: '

    data=get_api()
    global_card= CardFactory.thumbnail_card(ThumbnailCard(
        title="Global",
        text="""Total cases:\t{}\r\nBeing infected:\t{}\r\nDeaths:\t{}\r\nRecovered:\t{}\r\n""".format(str(data['global']['cases']),str(data['global']['infected']),str(data['global']['deaths']),str(data['global']['recovered'])),
        images=[
            CardImage(
                url="https://inkedin.com/wp-content/uploads/2020/03/earth-icon.png"
            )
        ],
        buttons=[
            CardAction(
                type=ActionTypes.open_url,
                title="More information",
                value="https://www.worldometers.info/coronavirus/",
            )
        ],
    ))
    vietnam_card= CardFactory.thumbnail_card(ThumbnailCard(
        title="Viet Nam",
        text="""Total cases:\t{}\r\nBeing infected:\t{}\r\nDeaths:\t{}\r\nRecovered: \t{}\r\n""".format(str(data['vietnam']['cases']),str(data['vietnam']['infected']),str(data['vietnam']['deaths']),str(data['vietnam']['recovered'])),
        images=[
            CardImage(
                url="https://cdn2.iconfinder.com/data/icons/world-flag-2/30/21-512.png"
            )
        ],
        buttons=[
            CardAction(
                type=ActionTypes.open_url,
                title="More information",
                value="https://corona.kompa.ai/",
            )
        ],
    ))
    anh=MessageFactory()
    reply = anh.list([],text=text)
    reply.attachment_layout = 'carousel'
    reply.attachments.append(global_card)
    reply.attachments.append(vietnam_card)
    return (reply,data['newest'])

class AdaptiveCardsBot(ActivityHandler):
    """
    This bot will respond to the user's input with an Adaptive Card. Adaptive Cards are a way for developers to
    exchange card content in a common and consistent way. A simple open card format enables an ecosystem of shared
    tooling, seamless integration between apps, and native cross-platform performance on any device. For each user
    interaction, an instance of this class is created and the OnTurnAsync method is called.  This is a Transient
    lifetime service. Transient lifetime services are created each time they're requested. For each Activity
    received, a new instance of this class is created. Objects that are expensive to construct, or have a lifetime
    beyond the single turn, should be carefully managed.
    """
    def __init__(self, conversation_references: Dict[str, ConversationReference]):
        self.conversation_references = conversation_references

    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    f"Hello everybody. I'm Corona. "
                    f"Ready to bring to you newest information about corona all over the world and Viet Nam. "
                    f"Type \"corona\" anytime to get the information."
                )

    async def on_message_activity(self, turn_context: TurnContext):
        self._add_conversation_reference(turn_context.activity)
        reply=generate_reply('reply')
        await turn_context.send_activity('My pleasure. Here some information: ')
        await turn_context.send_activity(reply[0])
        await turn_context.send_activity(reply[1])

    async def on_conversation_update_activity(self, turn_context: TurnContext):
        self._add_conversation_reference(turn_context.activity)
        return await super().on_conversation_update_activity(turn_context)

    def _add_conversation_reference(self, activity: Activity):
        """
        This populates the shared Dictionary that holds conversation references. In this sample,
        this dictionary is used to send a message to members when /api/notify is hit.
        :param activity:
        :return:
        """
        conversation_reference = TurnContext.get_conversation_reference(activity)
        self.conversation_references[
            conversation_reference.user.id
        ] = conversation_reference

class MessageFactory:
    """
    A set of utility functions designed to assist with the formatting of the various message types a
    bot can return.
    """

    @staticmethod
    def text(
        text: str,
        speak: str = None,
        input_hint: Union[InputHints, str] = InputHints.accepting_input,
    ) -> Activity:
        """
        Returns a simple text message.

        :Example:
        message = MessageFactory.text('Greetings from example message')
        await context.send_activity(message)

        :param text:
        :param speak:
        :param input_hint:
        :return:
        """
        message = Activity(type=ActivityTypes.message, text=text, input_hint=input_hint)
        if speak:
            message.speak = speak

        return message

    @staticmethod
    def suggested_actions(
        actions: List[CardAction],
        text: str = None,
        speak: str = None,
        input_hint: Union[InputHints, str] = InputHints.accepting_input,
    ) -> Activity:
        """
        Returns a message that includes a set of suggested actions and optional text.

        :Example:
        message = MessageFactory.suggested_actions([CardAction(title='a', type=ActionTypes.im_back, value='a'),
                                                    CardAction(title='b', type=ActionTypes.im_back, value='b'),
                                                    CardAction(title='c', type=ActionTypes.im_back, value='c')],
                                                    'Choose a color')
        await context.send_activity(message)

        :param actions:
        :param text:
        :param speak:
        :param input_hint:
        :return:
        """
        actions = SuggestedActions(actions=actions)
        message = Activity(
            type=ActivityTypes.message, input_hint=input_hint, suggested_actions=actions
        )
        if text:
            message.text = text
        if speak:
            message.speak = speak
        return message

    @staticmethod
    def attachment(
        attachment: Attachment,
        text: str = None,
        speak: str = None,
        input_hint: Union[InputHints, str] = None,
    ):
        """
        Returns a single message activity containing an attachment.

        :Example:
        message = MessageFactory.attachment(CardFactory.hero_card(HeroCard(title='White T-Shirt',
                                                                  images=[CardImage(url=
                                                                    'https://example.com/whiteShirt.jpg'
                                                                    )],
                                                                  buttons=[CardAction(title='buy')])))
        await context.send_activity(message)

        :param attachment:
        :param text:
        :param speak:
        :param input_hint:
        :return:
        """
        return attachment_activity(
            AttachmentLayoutTypes.list, [attachment], text, speak, input_hint
        )

    @staticmethod
    def list(
        attachments: List[Attachment],
        text: str = None,
        speak: str = None,
        input_hint: Union[InputHints, str] = None,
    ) -> Activity:
        """
        Returns a message that will display a set of attachments in list form.

        :Example:
        message = MessageFactory.list([CardFactory.hero_card(HeroCard(title='title1',
                                                             images=[CardImage(url='imageUrl1')],
                                                             buttons=[CardAction(title='button1')])),
                                       CardFactory.hero_card(HeroCard(title='title2',
                                                             images=[CardImage(url='imageUrl2')],
                                                             buttons=[CardAction(title='button2')])),
                                       CardFactory.hero_card(HeroCard(title='title3',
                                                             images=[CardImage(url='imageUrl3')],
                                                             buttons=[CardAction(title='button3')]))])
        await context.send_activity(message)

        :param attachments:
        :param text:
        :param speak:
        :param input_hint:
        :return:
        """
        return attachment_activity(
            AttachmentLayoutTypes.list, attachments, text, speak, input_hint
        )

    @staticmethod
    def carousel(
        attachments: List[Attachment],
        text: str = None,
        speak: str = None,
        input_hint: Union[InputHints, str] = None,
    ) -> Activity:
        """
        Returns a message that will display a set of attachments using a carousel layout.

        :Example:
        message = MessageFactory.carousel([CardFactory.hero_card(HeroCard(title='title1',
                                                                 images=[CardImage(url='imageUrl1')],
                                                                 buttons=[CardAction(title='button1')])),
                                           CardFactory.hero_card(HeroCard(title='title2',
                                                                 images=[CardImage(url='imageUrl2')],
                                                                 buttons=[CardAction(title='button2')])),
                                           CardFactory.hero_card(HeroCard(title='title3',
                                                                 images=[CardImage(url='imageUrl3')],
                                                                 buttons=[CardAction(title='button3')]))])
        await context.send_activity(message)

        :param attachments:
        :param text:
        :param speak:
        :param input_hint:
        :return:
        """
        return attachment_activity(
            AttachmentLayoutTypes.carousel, attachments, text, speak, input_hint
        )

    @staticmethod
    def content_url(
        url: str,
        content_type: str,
        name: str = None,
        text: str = None,
        speak: str = None,
        input_hint: Union[InputHints, str] = None,
    ):
        """
        Returns a message that will display a single image or video to a user.

        :Example:
        message = MessageFactory.content_url('https://example.com/hawaii.jpg', 'image/jpeg',
                                             'Hawaii Trip', 'A photo from our family vacation.')
        await context.send_activity(message)

        :param url:
        :param content_type:
        :param name:
        :param text:
        :param speak:
        :param input_hint:
        :return:
        """
        attachment = Attachment(content_type=content_type, content_url=url)
        if name:
            attachment.name = name
        return attachment_activity(
            AttachmentLayoutTypes.list, [attachment], text, speak, input_hint
        )
