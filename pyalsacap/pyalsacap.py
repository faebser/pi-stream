#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#############################################################################
## PyAlsaCap
## inspired from alsacap written by Volker Schatz
## http://www.volkerschatz.com/noise/alsacap.c
##
## Author:Thomas Debesse
## Last edit: 20130310
## Licence: ISC
##
## Copyright (c) 2013 Thomas Debesse <dev@illwieckz.net>
##
## Permission to use, copy, modify, and/or distribute this software for any
## purpose with or without fee is hereby granted, provided that the above
## copyright notice and this permission notice appear in all copies. 
##
## The software is provided "as is" and the author disclaims all warranties
## with regard to this software including all implied warranties of
## merchantability and fitness. in no event shall the author be liable for
## any special, direct, indirect, or consequential damages or any damages
## whatsoever resulting from loss of use, data or profits, whether in an
## action of contract, negligence or other tortious action, arising out or
## in connection with the use or performance of this software.
#############################################################################

from ctypes import *

#############################################################################
## this class defines some ALSA constants and configures libasound library
#############################################################################

class Libasound(object):

	def __init__(self):	
		pass

	def Lib(self):
		libasound = cdll.LoadLibrary("libasound.so.2")

		libasound.snd_ctl_card_info_get_id.restype = c_char_p
		libasound.snd_ctl_card_info_get_name.restype = c_char_p
		libasound.snd_pcm_info_get_id.restype = c_char_p
		libasound.snd_pcm_info_get_name.restype = c_char_p
		libasound.snd_pcm_info_get_subdevice_name.restype = c_char_p
		libasound.snd_pcm_format_name.restype = c_char_p
		libasound.snd_pcm_format_mask_test.restype = c_bool

		return libasound

	SND_PCM_FORMAT_S8 = c_int(0)
	SND_PCM_FORMAT_U8 = c_int(1)
	SND_PCM_FORMAT_S16_LE = c_int(2)
	SND_PCM_FORMAT_S16_BE = c_int(3)
	SND_PCM_FORMAT_U16_LE = c_int(4)
	SND_PCM_FORMAT_U16_BE = c_int(5)
	SND_PCM_FORMAT_S24_LE = c_int(6)
	SND_PCM_FORMAT_S24_BE = c_int(7)
	SND_PCM_FORMAT_U24_LE = c_int(8)
	SND_PCM_FORMAT_U24_BE = c_int(9)
	SND_PCM_FORMAT_S32_LE = c_int(10)
	SND_PCM_FORMAT_S32_BE = c_int(11)
	SND_PCM_FORMAT_U32_LE = c_int(12)
	SND_PCM_FORMAT_U32_BE = c_int(13)
	SND_PCM_FORMAT_FLOAT_LE = c_int(14)
	SND_PCM_FORMAT_FLOAT_BE = c_int(15)
	SND_PCM_FORMAT_FLOAT64_LE = c_int(16)
	SND_PCM_FORMAT_FLOAT64_BE = c_int(17)
	SND_PCM_FORMAT_IEC958_SUBFRAME_LE = c_int(18)
	SND_PCM_FORMAT_IEC958_SUBFRAME_BE = c_int(19)
	SND_PCM_FORMAT_MU_LAW = c_int(20)
	SND_PCM_FORMAT_A_LAW = c_int(21)
	SND_PCM_FORMAT_IMA_ADPCM = c_int(22)
	SND_PCM_FORMAT_MPEG = c_int(23)
	SND_PCM_FORMAT_GSM = c_int(24)
	SND_PCM_FORMAT_SPECIAL = c_int(31)
	SND_PCM_FORMAT_S24_3LE = c_int(32)
	SND_PCM_FORMAT_S24_3BE = c_int(33)
	SND_PCM_FORMAT_U24_3LE = c_int(34)
	SND_PCM_FORMAT_U24_3BE = c_int(35)
	SND_PCM_FORMAT_S20_3LE = c_int(36)
	SND_PCM_FORMAT_S20_3BE = c_int(37)
	SND_PCM_FORMAT_U20_3LE = c_int(38)
	SND_PCM_FORMAT_U20_3BE = c_int(39)
	SND_PCM_FORMAT_S18_3LE = c_int(40)
	SND_PCM_FORMAT_S18_3BE = c_int(41)
	SND_PCM_FORMAT_U18_3LE = c_int(42)
	SND_PCM_FORMAT_U18_3BE = c_int(43)
	SND_PCM_FORMAT_S16 = c_int(2)
	SND_PCM_FORMAT_U16 = c_int(4)
	SND_PCM_FORMAT_S24 = c_int(6)
	SND_PCM_FORMAT_U24 = c_int(8)
	SND_PCM_FORMAT_S32 = c_int(10)
	SND_PCM_FORMAT_U32 = c_int(12)
	SND_PCM_FORMAT_FLOAT = c_int(14)
	SND_PCM_FORMAT_FLOAT64 = c_int(16)
	SND_PCM_FORMAT_IEC958_SUBFRAME = c_int(18)
	SND_PCM_FORMAT_LAST = SND_PCM_FORMAT_U18_3BE

	SND_PCM_NONBLOCK = c_int(0x00000001)

	SND_PCM_STREAM_PLAYBACK = c_int(0)
	SND_PCM_STREAM_CAPTURE = c_int(1)
	SND_PCM_STREAM_LAST = SND_PCM_STREAM_CAPTURE

	format_list = {
		"S8": SND_PCM_FORMAT_S8,
		"U8": SND_PCM_FORMAT_U8,
		"S16_LE": SND_PCM_FORMAT_S16_LE,
		"S16_BE": SND_PCM_FORMAT_S16_BE,
		"U16_LE": SND_PCM_FORMAT_U16_LE,
		"U16_BE": SND_PCM_FORMAT_U16_BE,
		"S24_LE": SND_PCM_FORMAT_S24_LE,
		"S24_BE": SND_PCM_FORMAT_S24_BE,
		"U24_LE": SND_PCM_FORMAT_U24_LE,
		"U24_BE": SND_PCM_FORMAT_U24_BE,
		"S32_LE": SND_PCM_FORMAT_S32_LE,
		"S32_BE": SND_PCM_FORMAT_S32_BE,
		"U32_LE": SND_PCM_FORMAT_U32_LE,
		"U32_BE": SND_PCM_FORMAT_U32_BE,
		"FLOAT_LE": SND_PCM_FORMAT_FLOAT_LE,
		"FLOAT_BE": SND_PCM_FORMAT_FLOAT_BE,
		"FLOAT64_LE": SND_PCM_FORMAT_FLOAT64_LE,
		"FLOAT64_BE": SND_PCM_FORMAT_FLOAT64_BE,
		"IEC958_SUBFRAME_LE": SND_PCM_FORMAT_IEC958_SUBFRAME_LE,
		"IEC958_SUBFRAME_BE": SND_PCM_FORMAT_IEC958_SUBFRAME_BE,
		"MU_LAW": SND_PCM_FORMAT_MU_LAW,
		"A_LAW": SND_PCM_FORMAT_A_LAW,
		"IMA_ADPCM": SND_PCM_FORMAT_IMA_ADPCM,
		"MPEG": SND_PCM_FORMAT_MPEG,
		"GSM": SND_PCM_FORMAT_GSM,
		"SPECIAL": SND_PCM_FORMAT_SPECIAL,
		"S24_3LE": SND_PCM_FORMAT_S24_3LE,
		"S24_3BE": SND_PCM_FORMAT_S24_3BE,
		"U24_3LE": SND_PCM_FORMAT_U24_3LE,
		"U24_3BE": SND_PCM_FORMAT_U24_3BE,
		"S20_3LE": SND_PCM_FORMAT_S20_3LE,
		"S20_3BE": SND_PCM_FORMAT_S20_3BE,
		"U20_3LE": SND_PCM_FORMAT_U20_3LE,
		"U20_3BE": SND_PCM_FORMAT_U20_3BE,
		"S18_3LE": SND_PCM_FORMAT_S18_3LE,
		"S18_3BE": SND_PCM_FORMAT_S18_3BE,
		"U18_3LE": SND_PCM_FORMAT_U18_3LE,
		"U18_3BE": SND_PCM_FORMAT_U18_3BE,
		"S16": SND_PCM_FORMAT_S16,
		"U16": SND_PCM_FORMAT_U16,
		"S24": SND_PCM_FORMAT_S24,
		"U24": SND_PCM_FORMAT_U24,
		"S32": SND_PCM_FORMAT_S32,
		"U32": SND_PCM_FORMAT_U32,
		"FLOAT": SND_PCM_FORMAT_FLOAT,
		"FLOAT64": SND_PCM_FORMAT_FLOAT64,
		"IEC958_SUBFRAME": SND_PCM_FORMAT_IEC958_SUBFRAME
	}

#############################################################################
## this class extends dict type to store cards informations plus stream type
#############################################################################

class Cards(dict):
	def __init__(self, stream = "playback"):
		self.stream = stream

#############################################################################
## this class gets cards informations
#############################################################################

class Inspector(object):

	def __init__(self):
		self.Alsa = Libasound()
		self.libasound = self.Alsa.Lib()

	def GetCards(self, stream = "playback"):
		c_stream = c_int()

		if stream == "playback":
			c_stream = self.Alsa.SND_PCM_STREAM_PLAYBACK
		elif stream == "capture":
			c_stream = self.Alsa.SND_PCM_STREAM_CAPTURE
		else:
			raise Exception("bad stream name")

		cards = Cards(stream)

		c_card = c_int()
		c_dev = c_int()
		c_min = c_uint()
		c_max = c_uint()
		c_handle = c_void_p()
		c_pcm = c_void_p()
		c_info = (c_void_p * int(self.libasound.snd_ctl_card_info_sizeof() / sizeof(c_void_p)))()
		c_pcminfo = (c_void_p * int(self.libasound.snd_pcm_info_sizeof() / sizeof(c_void_p)))()
		c_pars = (c_void_p * int(self.libasound.snd_pcm_hw_params_sizeof() / sizeof(c_void_p)))()
		c_fmask = (c_void_p * int(self.libasound.snd_pcm_format_mask_sizeof() / sizeof(c_void_p)))()

		# card enumeration
		c_card.value = -1
		if self.libasound.snd_card_next(byref(c_card)) < 0:
			return cards
		else:
			while c_card.value >= 0:
				card = {}
				cards[c_card.value] = card

				hwdev = "hw:" + str(c_card.value)
				b_hwdev = create_string_buffer(str.encode(hwdev))

				err = self.libasound.snd_ctl_open(byref(c_handle), b_hwdev, c_card)
				if err < 0:
					self.libasound.snd_ctl_close(c_handle)
					pass
				else:
					self.libasound.snd_ctl_card_info(c_handle, c_info)

					card["id"] = bytes.decode(self.libasound.snd_ctl_card_info_get_id(c_info))
					card["name"] = bytes.decode(self.libasound.snd_ctl_card_info_get_name(c_info))

					# device enumeration
					devices = {}
					card["devices"] = devices

					c_dev.value = -1
					if self.libasound.snd_ctl_pcm_next_device(c_handle, byref(c_dev)) < 0:
						self.libasound.snd_ctl_close(handle)
						pass
					else:
						while c_dev.value >= 0:

							self.libasound.snd_pcm_info_set_device(c_pcminfo, c_dev)
							self.libasound.snd_pcm_info_set_subdevice(c_pcminfo, 0)
							self.libasound.snd_pcm_info_set_stream(c_pcminfo, c_stream)

							# count subdevices
							err = self.libasound.snd_ctl_pcm_info(c_handle, c_pcminfo)
							if not err < 0:
								device = {}
								devices[c_dev.value] = device
								device["id"] = bytes.decode(self.libasound.snd_pcm_info_get_id(c_pcminfo))
								device["name"] = bytes.decode(self.libasound.snd_pcm_info_get_name(c_pcminfo))

								nsubd = self.libasound.snd_pcm_info_get_subdevices_avail(c_pcminfo)
								device["subdevices_available"] = nsubd

								nsubd = self.libasound.snd_pcm_info_get_subdevices_count(c_pcminfo)
								if not nsubd < 0:

									# open sound device
									hwdev = "hw:" + str(c_card.value) + ',' + str(c_dev.value)
									b_hwdev = create_string_buffer(str.encode(hwdev))
									err = self.libasound.snd_pcm_open(byref(c_pcm), b_hwdev, c_stream, self.Alsa.SND_PCM_NONBLOCK)
									if not err < 0:

										# obtain hardware parameters
										err = self.libasound.snd_pcm_hw_params_any(c_pcm, c_pars)
										if err < 0:
											self.libasound.snd_pcm_close(c_pcm)
											pass
										else:

											# obtain channels min and max
											self.libasound.snd_pcm_hw_params_get_channels_min(c_pars, byref(c_min))
											self.libasound.snd_pcm_hw_params_get_channels_max(c_pars, byref(c_max))
											device["channels"] = [c_min.value, c_max.value]

											# obtain rate min and max
											self.libasound.snd_pcm_hw_params_get_rate_min(c_pars, byref(c_min))
											self.libasound.snd_pcm_hw_params_get_rate_max(c_pars, byref(c_max))
											device["rate"] = [c_min.value, c_max.value]

											# obtain formats
											self.libasound.snd_pcm_hw_params_get_format_mask(c_pars, c_fmask)
											formats = self.DecodeAlsaFormatMask(c_fmask)
											device["formats"] = formats

											self.libasound.snd_pcm_close(c_pcm)

											# *pcm = NULL
											c_pcm.value = None

											# enumerate subdevices
											subdevices = {}
											device["subdevices"] = subdevices

											for subd in range(0, nsubd):
												subdevice = {}  
												self.libasound.snd_pcm_info_set_subdevice(c_pcminfo, c_int(subd))
												subd_name = bytes.decode(self.libasound.snd_pcm_info_get_subdevice_name(c_pcminfo))
												subdevice["name"] = subd_name
												
												subdevices[subd] = subdevice
											# end subdevice enumeration

							if self.libasound.snd_ctl_pcm_next_device(c_handle, byref(c_dev)) < 0:
								break
						self.libasound.snd_ctl_close(c_handle)
					# end device enumeration

					if self.libasound.snd_card_next(byref(c_card)) < 0:
						break
		# end card enumeration

		return cards

	def DecodeAlsaFormatMask(self, c_fmask):
		formats = []
		for fmt in range(0, self.Alsa.SND_PCM_FORMAT_LAST.value):
			if self.libasound.snd_pcm_format_mask_test(c_fmask, c_int(fmt)):
				formats.append(bytes.decode(self.libasound.snd_pcm_format_name(c_int(fmt))))
		return formats

#############################################################################
## this class prints cards informations
#############################################################################

class Descriptor(object):

	def __init__(self):
		pass

	def PrintCards(self, cards):

		print("*** Scanning for ", end='')
		if cards.stream == "capture":
			print("recording", end='')
		else:
			print("playback", end='')

		print(" devices ***")

		for numcard in cards:
			# print cards
			card = cards[numcard]
			print("Card " + str(numcard) + ", ID `" + card["id"] + "', name `" + card["name"] + '\'')

			devices = card["devices"]
			for numdev in devices:
				# print devices
				device = devices[numdev]
				print("  Device " + str(numdev) + ", ID `" + device["id"] + "', name `" + device["name"] + "', " + str(len(device["subdevices"])) + " subdevices (" + str(device["subdevices_available"]) + " available)")

				# print channels
				channels = device["channels"]
				print("    ", end='')
				if channels[0] == channels[1]:
					if channels[0] == 1:
						print('1', end='')
					else:
						print(str(channels[0]), end='')
				else:
					print(str(channels[0] + ".." + str(channels[1]), end=''))

				if channels[1] == 1:
					print(" channel", end='')
				else:
					print(" channels", end='')

				# print sampling rate
				rate = device["rate"]
				print(", sampling rate " + str(rate[0]) + ".." + str(rate[1]) + " Hz")

				# print formats
				print("    Sample formats: ", end='')

				formats = device["formats"]
				for a_format in formats:
					# print format
					print(a_format, end='')
					if len(formats) > 1:
						print(", ", end='')
				print('')

				# print subdevices
				subdevices = device["subdevices"]
				for numsubdev in subdevices:
					# print subdevice
					subdevice = subdevices[numsubdev]
					print("      Subdevice " + str(numsubdev) + ", name `" + subdevice["name"] + "'")

#############################################################################
## this module can be executed as a script
#############################################################################

if __name__ == "__main__":
	import sys

	insp = Inspector()
	desc = Descriptor()

	if len(sys.argv) == 2:
		if sys.argv[1] == "-R":
			cards = insp.GetCards("capture")
	else:
		cards = insp.GetCards()

	desc.PrintCards(cards)

# vim: set tabstop=4
