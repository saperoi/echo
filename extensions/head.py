import lightbulb
import hikari
import comm

plugin = lightbulb.Plugin('head', 'The bot is plural don\'t you know!')

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)

letterbot_response = {
    "": "Hi! I'm LettərBot & I love playing with the alphabet! ^-^\nI was born on the 22nd of July, 2018; originally with discord.js--commando and my prefix back then was `ae!`",
    "and": "Traditionally, when reciting the alphabet in English-speaking schools, any letter that could also be used as a word in itself (A, I, and, at one point, O) was repeated with the Latin expression per se (by itself). ",
    "ampersand": "Traditionally, when reciting the alphabet in English-speaking schools, any letter that could also be used as a word in itself (A, I, and, at one point, O) was repeated with the Latin expression per se (by itself). ",
    "ash": "Ææ is a grapheme, formed from the letters a and e, originally a ligature representing the Latin diphthong ae. It has been promoted to the full status of a letter in the alphabets of some languages, including Danish, Norwegian, Icelandic, and Faroese.",
    "aesc": "Ææ is a grapheme, formed from the letters a and e, originally a ligature representing the Latin diphthong ae. It has been promoted to the full status of a letter in the alphabets of some languages, including Danish, Norwegian, Icelandic, and Faroese.",
    "edh": "Ðð called Edh or Edd is a letter used in Old English, Middle English, Icelandic, Faroese and Elfdalian. The lowercase version has been adopted to represent a voiced dental fricative in the International Phonetic Alphabet. The lowercase is sometimes used in mathematics and engineering textbooks as a symbol for a spin-weighted partial derivative. This operator gives rise to spin-weighted spherical harmonics.",
    "edd": "Ðð called Edh or Edd is a letter used in Old English, Middle English, Icelandic, Faroese and Elfdalian. The lowercase version has been adopted to represent a voiced dental fricative in the International Phonetic Alphabet. The lowercase is sometimes used in mathematics and engineering textbooks as a symbol for a spin-weighted partial derivative. This operator gives rise to spin-weighted spherical harmonics.",
    "eng": "Ŋŋ is a letter of the Latin alphabet, used to represent a velar nasal (as in English singing) in the written form of some languages and in the International Phonetic Alphabet.",
    "engma": "Ŋŋ is a letter of the Latin alphabet, used to represent a velar nasal (as in English singing) in the written form of some languages and in the International Phonetic Alphabet.",
    "eszett": "In German orthography, the grapheme ß, called Eszett (IPA: [ɛsˈtsɛt]) or scharfes S (IPA: [ˈʃaɐ̯fəs ˈʔɛs], [ˈʃaːfəs ˈʔɛs], lit. sharp S), represents the [s] phoneme in Standard German, specifically when following long vowels and diphthongs, while ss is used after short vowels. The name Eszett combines the names of the letters of s (Es) and z (Zett) in German.",
    "sz": "In German orthography, the grapheme ß, called Eszett (IPA: [ɛsˈtsɛt]) or scharfes S (IPA: [ˈʃaɐ̯fəs ˈʔɛs], [ˈʃaːfəs ˈʔɛs], lit. sharp S), represents the [s] phoneme in Standard German, specifically when following long vowels and diphthongs, while ss is used after short vowels. The name Eszett combines the names of the letters of s (Es) and z (Zett) in German.",
    "ethel": "Œœ is a Latin alphabet grapheme, a ligature of o and e. In medieval and early modern Latin, it was used to represent the Greek diphthong οι and in a few non-Greek words, usages that continue in English and French. In French, it is also used in some non-learned words, representing then mid-front rounded vowel-sounds, rather than sounding the same as é or è, those being its traditional French values in the words borrowed from or via Latin.",
    "whligerature": "Ŵ = W-H Ligature = Replaces White with Ŵite = Still used in Chichewa in words like Malaŵi meaning Malawi",
    "gha": "Ƣƣ has been used in the Latin orthographies of various, mostly Turkic languages, such as Azeri or the Jaꞑalif orthography for Tatar.[1] It usually represents a voiced velar fricative [ɣ] but is sometimes used for a voiced uvular fricative [ʁ]. All orthographies using it have been phased out, so the letter is not well-supported in fonts. It can still be seen in pre-1983 books published by the People’s Republic of China.",
    "longs": "ſ The long, medial, or descending s (ſ) is an archaic form of the lower case letter s. It replaced a single s, or the first in a double s, at the beginning or in the middle of a word (e.g. ſinfulneſs for sinfulness and ſucceſsful for successful). The modern letterform is known as the short, terminal, or round s.",
    "schwa": "Əə is an additional letter of the Latin alphabet, used in the Azerbaijani language and in the hən̓q̓əmin̓əm̓ dialect of Halkomelem. Both the majuscule and minuscule forms of this letter are based on the form of an upside down e, while the Pan-Nigerian alphabet pairs the same lowercase letter with Ǝ.",
    "slasho": "Øø is a vocal and the 28th letter in the Danish-Norwegian alphabet . It is also included in the Faroese alphabet and has arisen as a contraction between o and e (like the French Œ ). In the international phonetic alphabet it denotes a rounded semi-closed fortungevokal that corresponds to the Danish island.",
    "that": "Ꝥ is just an old remix of the word that, it's just a thorn with a dash through the top.",
    "thorn": "Þþ is a letter in the Old English, Gothic, Old Norse and modern Icelandic alphabets. It is pronounced as either a voiceless dental fricative [θ] or the voiced counterpart of it [ð]. However, in modern Icelandic, it is pronounced as a laminal voiceless alveolar non-sibilant fricative [θ̠]. If you see 'Ye' somewhere its not a Y but the letter Thorn.",
    "chorn": "Þþ is a letter in the Old English, Gothic, Old Norse and modern Icelandic alphabets. It is pronounced as either a voiceless dental fricative [θ] or the voiced counterpart of it [ð]. However, in modern Icelandic, it is pronounced as a laminal voiceless alveolar non-sibilant fricative [θ̠]. If you see 'Ye' somewhere its not a Y but the letter Thorn.",
    "vend": "Ꝩꝩ (vend) is a letter of Old Norse. It was used to represent the sounds /u/, /v/, and /w/.",
    "wynn": "Ƿƿ (wynn,wen,ƿynn,ƿen) is a letter of the Old English alphabet, where it is used to represent the sound /w/. This letter came to existenc when there was in Old English no letter for the sound w.",
    "wen": "Ƿƿ (wynn,wen,ƿynn,ƿen) is a letter of the Old English alphabet, where it is used to represent the sound /w/. This letter came to existenc when there was in Old English no letter for the sound w.",
    "yogh": "Ȝȝ was used in Middle English and Older Scots, representing y (/j/) and various velar phonemes. It was derived from the Old English form of the letter g."
}

@plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option("letter", "The letter to get information about", type=str, default="", choices=list(letterbot_response.keys()))
@lightbulb.command("letterbot", "LetterBot!", aliases=["LETTERBOT", "l!"])
@lightbulb.implements(lightbulb.PrefixCommandGroup)
async def letterbot(ctx: lightbulb.Context):
    comm.log_com(ctx)
    await comm.plurality_webhook_send(ctx, "letterbot", letterbot_response[ctx.options.letter.lower()])
    # Respond with help command

"""
@letterbot.child
@lightbulb.command("ena", "Enables tags", aliases=["ENA"])
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def letterbot(ctx: lightbulb.Context):
    comm.log_com(ctx)
"""