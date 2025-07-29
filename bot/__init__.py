def register_handlers(dp):
    dp.message(Command("start"))(cmd_start)
    dp.message(Command("help"))(cmd_help)
    dp.message(lambda m: m.content_type == 'text')(handle_text)
    dp.message(lambda m: m.content_type == 'photo')(lambda m: handle_photo(m, dp.bot))
    dp.message(lambda m: m.content_type == 'document')(handle_document)
