# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import json
import os
import random
from typing import List, Union
from botbuilder.core import ActivityHandler, TurnContext, CardFactory
from botbuilder.schema import ChannelAccount, Attachment, Activity, ActivityTypes
from botbuilder.schema import (
    ActionTypes,
    Attachment,
    AnimationCard,
    AudioCard,
    HeroCard,
    VideoCard,
    ReceiptCard,
    SigninCard,
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
def get_api():
    API_ENDPOINT_all = "https://corona.lmao.ninja/all"
    API_ENDPOINT_country = 'https://corona.lmao.ninja/countries'
    # sending post request and saving response as response object 
    global_statistic = requests.get(url = API_ENDPOINT_all).json()
    global_statistic['being_infected']=global_statistic['cases']-global_statistic['deaths']-global_statistic['recovered']
    vietnam_statistic = [a for a in requests.get(url = API_ENDPOINT_country).json() if a['country']=='Vietnam'][0]
    vietnam_statistic={key:vietnam_statistic[key] for key in ['cases','deaths','recovered']}
    vietnam_statistic['being_infected']=vietnam_statistic['cases']-vietnam_statistic['deaths']-vietnam_statistic['recovered']
    return {'global':global_statistic,'vietnam':vietnam_statistic}


CARDS = [
    "resources/FlightItineraryCard.json",
    "resources/ImageGalleryCard.json",
    "resources/LargeWeatherCard.json",
    "resources/RestaurantCard.json",
    "resources/SolitaireCard.json"
]

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

    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    f"Hello everybody. I'm Corona"
                    f"Ready to bring to you newest information about corona all over the world and Viet Nam"
                    f"Type \"corona\" anytime to get the information."
                )

    async def on_message_activity(self, turn_context: TurnContext):
        # if turn_context.activity.text=="corona":
        data=get_api()
        #     message = Activity(
        #         text="My pleasure. Here some information:",
        #         type=ActivityTypes.message,
        #         attachments=[CardFactory.receipt_card(ReceiptCard(
        #     items=[ReceiptItem(
        #             title="CORONA STATISTIC (LIVE)",
        #             # price="$45.00",
        #             # quantity="720",
        #             image=CardImage(
        #                 url="https://www.sifo-ltd.com/hs-fs/hubfs/Images/Icons/011-world.png?width=512&name=011-world.png"
        #             )
        #         ),
        #         ReceiptItem(
        #             title="Global",
        #             # price="$45.00",
        #             # quantity="720",
        #             # image=CardImage(
        #             #     url="https://cdn2.iconfinder.com/data/icons/world-flag-2/30/21-512.png"
        #             # )
        #         ),
        #         ReceiptItem(
        #             title="Total cases: ",
        #             price=str(data['global']['cases']),
        #             ),
        #         ReceiptItem(
        #             title="Deaths: ",
        #             price=str(data['global']['deaths']),
        #             ),
        #         ReceiptItem(
        #             title="Being infected:",
        #             price=str(data['global']['being_infected']),
        #             ),
        #         ReceiptItem(
        #             title="Recovered: ",
        #             price=str(data['global']['recovered']),
        #             ),
        #         ReceiptItem(
        #         text="hi",
        #         title='______________'
        #         ),
        #         ReceiptItem(
        #             title="Viet Nam",
        #             # price="$45.00",
        #             # quantity="720",
        #             # image=CardImage(
        #             #     url="https://cdn2.iconfinder.com/data/icons/world-flag-2/30/21-512.png"
        #             # )
        #         ),
        #         ReceiptItem(
        #             subtitle="Total cases: ",
        #             price=str(data['vietnam']['cases']),
        #             ),
        #         ReceiptItem(
        #             subtitle="Deaths: ",
        #             price=str(data['vietnam']['deaths']),
        #             ),
        #         ReceiptItem(
        #             subtitle="Being infected:",
        #             price=str(data['vietnam']['being_infected']),
        #             ),
        #         ReceiptItem(
        #             subtitle="Recovered: ",
        #             price=str(data['vietnam']['recovered']),
        #             ),
        #     ],
        #     total=" ",
        #     buttons=[
        #         CardAction(
        #             type=ActionTypes.open_url,
        #             title="More Information",
        #             value="https://www.worldometers.info/coronavirus/",
        #         )
        #     ],
        # ))],
        #     )
        global_card= CardFactory.thumbnail_card(ThumbnailCard(
            title="Global",
            text="""Total cases:\t{}\r\nBeing infected:\t{}\r\nDeaths:\t{}\r\nRecovered:\t{}\r\n""".format(str(data['global']['cases']),str(data['global']['being_infected']),str(data['global']['deaths']),str(data['global']['recovered'])),
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
            text="""Total cases:\t{}\r\nBeing infected:\t{}\r\nDeaths:\t{}\r\nRecovered: \t{}\r\n""".format(str(data['vietnam']['cases']),str(data['vietnam']['being_infected']),str(data['vietnam']['deaths']),str(data['vietnam']['recovered'])),
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
        reply = MessageFactory.list([])
        reply.text="My pleasure. Here some information: "
        reply.attachment_layout = 'carousel'
        reply.attachments.append(global_card)
        reply.attachments.append(vietnam_card)
        await turn_context.send_activity(reply)

    def _create_adaptive_card_attachment(self) -> Attachment:
        """
        Load a random adaptive card attachment from file.
        :return:
        """
        random_card_index = random.randint(0, len(CARDS) - 1)
        card_path = os.path.join(os.getcwd(), CARDS[random_card_index])
        with open(card_path, "rb") as in_file:
            card_data = json.load(in_file)

        return CardFactory.adaptive_card(card_data)

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
