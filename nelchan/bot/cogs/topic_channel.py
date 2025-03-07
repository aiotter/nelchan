from discord.ext.commands import Bot, Cog, Context, group
from nelchan.adapter.repository_impl import (
    GuildRepositoryImpl,
    GuildRepositoryImplForMongo,
    TopicChannelRepositoryImpl,
    TopicChannelRepositoryImplForMongo,
)
from nelchan.usecase.inputport import (
    CreateTopicChannelCategoryInputData,
    CreateTopicChannelCategoryUseCase,
    InitTopicChannelCategoryInputData,
    InitTopicChannelCategoryUseCase,
    RegisterTopicChannelInputData,
    RegisterTopicChannelUseCase,
    SetTopicInputData,
    SetTopicUseCase,
    UnregisterTopicChannelInputData,
    UnregisterTopicChannelUseCase,
    UnsetTopicInputData,
    UnsetTopicUseCase,
)
from nelchan.usecase.interactor import (
    CreateTopicChannelCategoryInteractor,
    InitTopicChannelCategoryInteractor,
    RegisterTopicChannelInteractor,
    SetTopicInteractor,
    UnregisterTopicChannelInteractor,
    UnsetTopicInteractor,
)
from nelchan.usecase.presenter import (
    CreateTopicChannelCategoryPresenter,
    RegisterTopicChannelPresneter,
    SetTopicPresenter,
    UnregisterTopicChannelPresneter,
    UnsetTopicPresenter,
)
from nelchan.usecase.presenter.topic_ch_presenter import (
    InitTopicChannelCategoryPresenter,
)


class Topic(Cog):
    def __init__(
        self,
        bot: Bot,
        create_category_usecase: CreateTopicChannelCategoryUseCase,
        init_category_usecase: InitTopicChannelCategoryUseCase,
        register_channel_usecase: RegisterTopicChannelUseCase,
        unregister_channel_usecase: UnregisterTopicChannelUseCase,
        set_topic_usecase: SetTopicUseCase,
        unset_topic_usecase: UnsetTopicUseCase,
    ) -> None:
        self.bot = bot
        self.create_category_usecase = create_category_usecase
        self.register_channel_usecase = register_channel_usecase
        self.unregister_channel_usecase = unregister_channel_usecase
        self.set_topic_usecase = set_topic_usecase
        self.unset_topic_usecase = unset_topic_usecase
        self.init_category_usecase = init_category_usecase

    @group(name="world", aliases=["w"])
    async def topic(self, ctx: Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send("正確なサブコマンドを指定してよねっ！")

    @topic.command(name="new")
    async def new_world(self, ctx: Context, category_name: str) -> None:
        """ワールド用カテゴリを生成するコマンド"""
        input_data = CreateTopicChannelCategoryInputData(category_name, ctx, self.bot)
        await self.create_category_usecase.handle(input_data)

    @topic.command(name="init")
    async def init_world(self, ctx: Context, category_id: str) -> None:
        """ワールド用カテゴリを生成するコマンド"""
        input_data = InitTopicChannelCategoryInputData(category_id, ctx, self.bot)
        await self.init_category_usecase.handle(input_data)

    @topic.command(name="register")
    async def register_channel(self, ctx: Context):
        """ワールド用チャンネルとして登録するコマンド"""
        input_data = RegisterTopicChannelInputData(ctx, self.bot)
        await self.register_channel_usecase.handle(input_data)

    @topic.command(name="unregister")
    async def unregister_channel(self, ctx: Context):
        """ワールド用チャンネルの登録を解除するコマンド"""
        input_data = UnregisterTopicChannelInputData(ctx, self.bot)
        await self.unregister_channel_usecase.handle(input_data)

    @topic.command(name="set", aliases=["s"])
    async def set_topic(self, ctx: Context, topic_title: str):
        """話題設定コマンド"""
        print("hekk")
        input_data = SetTopicInputData(topic_title, ctx, self.bot)
        await self.set_topic_usecase.handle(input_data)

    @topic.command(name="unset", aliases=["us"])
    async def unset_topic(self, ctx: Context):
        """話題設定解除コマンド"""
        input_data = UnsetTopicInputData(ctx, self.bot)
        await self.unset_topic_usecase.handle(input_data)


def setup(bot: Bot) -> None:
    import os

    environment = os.environ["ENV"]
    if environment == "dev":
        guild_repository = GuildRepositoryImplForMongo("nelchan", "channel")
        channel_repository = TopicChannelRepositoryImplForMongo("nelchan", "channel")
    elif environment == "prod":
        guild_repository = GuildRepositoryImpl("nelchan")
        channel_repository = TopicChannelRepositoryImpl("nelchan")

    bot.add_cog(
        Topic(
            bot,
            create_category_usecase=CreateTopicChannelCategoryInteractor(
                presenter=CreateTopicChannelCategoryPresenter(),
                repository=guild_repository,
            ),
            register_channel_usecase=RegisterTopicChannelInteractor(
                presenter=RegisterTopicChannelPresneter(),
                channel_repository=channel_repository,
                guild_repository=guild_repository,
            ),
            unregister_channel_usecase=UnregisterTopicChannelInteractor(
                presenter=UnregisterTopicChannelPresneter(),
                channel_repository=channel_repository,
                guild_repository=guild_repository,
            ),
            set_topic_usecase=SetTopicInteractor(
                presenter=SetTopicPresenter(),
                channel_repository=channel_repository,
                guild_repository=guild_repository,
            ),
            unset_topic_usecase=UnsetTopicInteractor(
                presenter=UnsetTopicPresenter(),
                channel_repository=channel_repository,
                guild_repository=guild_repository,
            ),
            init_category_usecase=InitTopicChannelCategoryInteractor(
                presenter=InitTopicChannelCategoryPresenter(),
                repository=guild_repository,
            ),
        )
    )
