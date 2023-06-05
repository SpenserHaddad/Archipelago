import asyncio
from collections.abc import Awaitable
from functools import partial
import logging
import os
from typing import Any, Callable, NoReturn

from CommonClient import ClientCommandProcessor, CommonContext
from MultiServer import CommandProcessor
import NetUtils
import Utils

import discord
from discord.ext import commands
from discord.ext.commands import Bot, Cog, command

from worlds.AutoWorld import AutoWorldRegister


logger = logging.getLogger("DiscordClient")

intents = discord.Intents(guild_messages=True, message_content=True)
discord_bot = Bot(command_prefix="!", intents=intents)

_MESSAGEABLE_CHANNEL = (
    discord.TextChannel
    | discord.VoiceChannel
    | discord.StageChannel
    | discord.Thread
    | discord.DMChannel
    | discord.PartialMessageable
    | discord.GroupChannel
)


class DiscordCommandCog(Cog):
    """Archipelago CLI commands for Discord

    Relays commands from Discord messages to the Archipelago client, and sends messages
    from the client to the appropriate channel.
    """

    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self._bot = bot
        self._ap_contexts: dict[int, DiscordContext] = {}

    @Cog.listener()
    async def on_ready(self):
        logger.info("Logged in as %s.", self._bot.user)

    @command()
    async def connect(self, ctx: commands.Context, ip: str, port: int, slot: str, password: str | None = None):
        logger.info(f"Connect called with {ctx}, {ip=}, {port=}.")

        server_address = f"archipelago://{ip}:{port}"
        ap_context_callback = partial(self._handle_ap_server_command, ctx.channel)
        ap_context = DiscordContext(server_address, password, ap_context_callback)
        ap_context.auth = slot
        ap_context.password = password
        await ap_context.connect()
        await ap_context.server_auth()
        logger.debug(f"Connected successfully, assigning to channel {ctx.channel.id}")
        self._ap_contexts[ctx.channel.id] = ap_context

    @connect.error
    async def connect_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingRequiredArgument):
            missing_arg = error.param.name
            logger.error(f"Connect command missing argument {missing_arg}.")
            await ctx.send(f"Connect `command` missing argument `{missing_arg}`.")

    @command()
    async def received(self, ctx: commands.Context):
        """List all received items."""
        ap_context = self._ap_contexts[ctx.channel.id]
        message_lines = [f"{len(ap_context.items_received)} received items:"]
        for idx, item in enumerate(ap_context.items_received, start=1):
            item_name = ap_context.item_names[item.item]
            player_name = ap_context.player_names[item.player]
            location_name = ap_context.location_names[item.location]
            message_lines.append(f"{idx}. {item_name} from {player_name} at {location_name}")
        await ctx.channel.send("\n".join(message_lines))

    @command()
    async def items(self, ctx: commands.Context):
        """List all item names for the currently running game."""
        ap_context = self._ap_contexts[ctx.channel.id]
        if not ap_context.game:
            await ctx.channel.send("No game set, cannot determine existing items.")
            return

        message_lines = [f"Item Names for {ap_context.game}:"]
        for idx, item in enumerate(AutoWorldRegister.world_types[ap_context.game].item_name_to_id, start=1):
            message_lines.append(f"{idx}. {item}")
        await ctx.channel.send("\n".join(message_lines))

    @command()
    async def locations(self, ctx: commands.Context):
        """List all location names for the currently running game."""
        ap_context = self._ap_contexts[ctx.channel.id]
        if not ap_context.game:
            await ctx.channel.send("No game set, cannot determine existing locations.")
            return

        message_lines = [f"Location Names for {ap_context.game}:"]
        for idx, location in enumerate(AutoWorldRegister.world_types[ap_context.game].location_name_to_id, start=1):
            message_lines.append(f"{idx}. {location}")
        await self._send_to_channel(ctx.channel, "\n".join(message_lines))

    @command()
    async def missing(self, ctx: commands.Context, filter_text=""):
        """List all missing location checks from your local game state.

        Can be given text, which will be used as a filter
        """
        ap_context = self._ap_contexts[ctx.channel.id]
        if not ap_context.game:
            await ctx.channel.send("No game set, cannot determine existing locations.")
            return
        count = 0
        checked_count = 0
        message_lines = []
        for location, location_id in AutoWorldRegister.world_types[ap_context.game].location_name_to_id.items():
            if filter_text and filter_text not in location:
                continue
            elif location_id < 0:
                continue
            elif location_id not in ap_context.locations_checked:
                if location_id in ap_context.missing_locations:
                    message_lines.append(f"Missing: {location}")
                    count += 1
                elif location_id in ap_context.checked_locations:
                    message_lines.append(f"Checked: {location}")
                    checked_count += 1
        if count:
            count_str = f"Found {count} missing location checks"
            if checked_count:
                count_str += f". {checked_count} location checks previously visited."
            message_lines.append(count_str)
        else:
            message_lines.append("No missing location checks found.")

        message_lines = [f"{len(ap_context.items_received)} received items:"]
        for idx, item in enumerate(ap_context.items_received, start=1):
            item_name = ap_context.item_names[item.item]
            player_name = ap_context.player_names[item.player]
            location_name = ap_context.location_names[item.location]
            message_lines.append(f"{idx}. {item_name} from {player_name} at {location_name}")
        await ctx.channel.send("\n".join(message_lines))

    async def _send_to_channel(self, channel: _MESSAGEABLE_CHANNEL, contents: str):
        # Discord only allows content of 2000 chars or less, which we can break.
        # Send in chunks if necessary.
        chunk_size = 1500
        chunks = []
        for chunk_start in range(0, len(contents), chunk_size):
            chunk = contents[chunk_start : chunk_start + chunk_size]
            chunks.append(chunk)
        for ch in chunks:
            await channel.send(ch)

    async def _handle_ap_server_command(
        self, channel: _MESSAGEABLE_CHANNEL, ctx: "DiscordContext", command: str, args: dict
    ):
        logger.debug(f"Handle command on {channel=}, {command=}, {args=}")
        if command == "RoomInfo":
            message_lines = [
                "Connected to server!",
                "Room Information:",
            ]
            message_lines.append(f"- Server protocol version: {ctx.server_version.as_simple_string()}")
            if "generator_version" in args:
                message_lines.append(f"- Generator version: {ctx.generator_version.as_simple_string()}")
            message_lines.append(f"- Tags: {', '.join(args['tags'])}")
            password_str = "Yes" if args["password"] else "No"
            message_lines.append(f"- Password required: {password_str}")
            message_lines.append(f"- !hint cost: {args['hint_cost']}")
            message_lines.append(f"- Hints per location checked: {args['location_check_points']}")
            await channel.send("\n".join(message_lines))
        elif command == "ConnectionRefused":
            errors = args["errors"]
            message_lines = ["Connection refused for the following reason(s):"]
            error_message_lines = []
            for err in errors:
                if err == "InvalidSlot":
                    error_message_lines.append(
                        f"Invalid Slot {ctx.auth}; please verify that you have connected to the correct world."
                    )
                elif err == "InvalidGame":
                    # This really shouldn't happen since we're a text-only client, but can't hurt to add.
                    error_message_lines.append(
                        f"Invalid Game {ctx.game}; please verify that you connected with the right game to the "
                        "correct world."
                    )
                elif err == "IncompatibleVersion":
                    error_message_lines.append(
                        f"Server reported your client version ({Utils.version_tuple}) as incompatible."
                    )
                elif err == "InvalidItemsHandling":
                    error_message_lines.append(
                        f"The item handling flags requested by the client ({ctx.items_handling:03b}) are not supported."
                    )
                else:
                    error_message_lines.append(f"An unexpected error: {err}.")
            message_lines.extend(f"- {eml}" for eml in error_message_lines)
            await channel.send("\n".join(message_lines))
        elif command == "Connected":
            if ctx.slot:
                ctx.game = ctx.slot_info[ctx.slot].game
            await channel.send(f"Connected to game on Team #{args['team']}, Slot #{args['slot']}")
        elif command == "ReceivedItems":
            pass
        elif command == "LocationInfo":
            pass
        elif command == "RoomUpdate":
            message_lines = []
            new_permissions: dict[str, int] | None = args.get("permissions")
            if new_permissions:
                message_lines.append("Permissions updated:")
                for name, permission_flag in new_permissions.items():
                    flag = NetUtils.Permission(permission_flag)
                    message_lines.append(f"- {name.capitalize()} permission: {flag.name}")
            if message_lines:
                await channel.send("\n".join(message_lines))

        elif command == "Print":
            await channel.send(args["text"])
        elif command == "PrintJSON":
            # TODO: Can we color or make this richer somehow? Maybe with embeds?
            json_str_segments = "".join(d["text"] for d in args["data"])
            await channel.send(json_str_segments)
        elif command == "DataPackage":
            pass
        elif command == "Bounced":
            pass
        elif command == "InvalidPacket":
            pass
        elif command == "Retrieved":
            pass
        elif command == "SetReply":
            pass


class DiscordCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def output(self, text: str):
        return super().output(text)


class DiscordContext(CommonContext):
    command_processor: type[CommandProcessor] = DiscordCommandProcessor
    game: str | None = None  # Connect to any game
    tags: set[str] = {"TextOnly"}
    items_handling = 0b111  # receive all items
    want_slot_data = False

    def __init__(
        self,
        server_address: str | None,
        password: str | None,
        on_command_received: Callable[["DiscordContext", str, dict[str, Any]], Awaitable[None]],
    ) -> None:
        super().__init__(server_address, password)
        self._received_room_info = asyncio.Event()
        self._on_command_received = on_command_received
        self._server_command_queue: asyncio.Queue[tuple[str, dict]] = asyncio.Queue()
        self._handle_commands_task: asyncio.Task[NoReturn] | None = None

    def on_package(self, cmd: str, args: dict):
        # logger.info(f"Package: {cmd=}, {args=}")
        self._server_command_queue.put_nowait((cmd, args))

        return super().on_package(cmd, args)

    def on_print_json(self, args: dict):
        logger.info(f"print json: {args=}")
        return super().on_print_json(args)

    async def connect(self, address: str | None = None) -> None:
        self._received_room_info.clear()
        self._handle_commands_task = asyncio.create_task(self._handle_commands())
        await super().connect(address)
        await self._received_room_info.wait()

    async def server_auth(self, password_requested: bool = False):
        await self.send_connect()

    async def _handle_commands(self):
        while True:
            cmd, args = await self._server_command_queue.get()
            if cmd == "RoomInfo":
                self._received_room_info.set()
            try:
                await self._on_command_received(self, cmd, args)
            except Exception:
                logger.exception(f"Bot raised an exception handling command {cmd}")
                raise


async def main():
    auth_token = os.environ["AP_DISCORD_TOKEN"]
    await discord_bot.add_cog(DiscordCommandCog(discord_bot))
    await discord_bot.start(auth_token)


if __name__ == "__main__":
    Utils.init_logging("DiscordClient")
    ap_logger = logging.getLogger("ap")
    ap_logger.setLevel(logging.DEBUG)
    # log_file_handler = logging.FileHandler("ap_discord_client.log")
    # logger.addHandler(log_file_handler)
    stream_handler = logging.StreamHandler()
    ap_logger.addHandler(stream_handler)
    asyncio.run(main())
