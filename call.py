"""
##########################################################################
*
*   Copyright © 2019-2021 Akashdeep Dhar <t0xic0der@fedoraproject.org>
*
*   This program is free software: you can redistribute it and/or modify
*   it under the terms of the GNU General Public License as published by
*   the Free Software Foundation, either version 3 of the License, or
*   (at your option) any later version.
*
*   This program is distributed in the hope that it will be useful,
*   but WITHOUT ANY WARRANTY; without even the implied warranty of
*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*   GNU General Public License for more details.
*
*   You should have received a copy of the GNU General Public License
*   along with this program.  If not, see <https://www.gnu.org/licenses/>.
*
##########################################################################
"""

import bs4 as btsp
import urllib.request as ulrq
import urllib.parse as ulpr


def fetch_channel_dict():
    try:
        source = ulrq.urlopen("https://meetbot-raw.fedoraproject.org").read()
        parse_object = btsp.BeautifulSoup(source, "html.parser")
        channel_dict = {}
        for channel in parse_object.find_all("a")[5:]:
            channel_dict[channel.string[0:-1]] = "https://meetbot-raw.fedoraproject.org" + "/" + channel.get("href")
        return True, channel_dict
    except Exception as expt:
        return False, {"exception": str(expt)}


def fetch_datetxt_dict(channel: str):
    try:
        source = ulrq.urlopen("https://meetbot-raw.fedoraproject.org" + "/" + channel).read()
        parse_object = btsp.BeautifulSoup(source, "html.parser")
        datetxt_dict = {}
        for datetxt in parse_object.find_all("a")[5:]:
            datetxt_dict[datetxt.string[0:-1]] = "https://meetbot-raw.fedoraproject.org" + "/" + channel + "/" + datetxt.get("href")
        return True, datetxt_dict
    except Exception as expt:
        return False, {"exception": str(expt)}


def fetch_meeting_dict(channel: str, datetxt: str):
    try:
        source = ulrq.urlopen("https://meetbot-raw.fedoraproject.org" + "/" + channel + "/" + datetxt + "/").read()
        parse_object = btsp.BeautifulSoup(source, "html.parser")
        meeting_dict = {}
        for meeting in parse_object.find_all("a")[5:]:
            if ".log.html" in meeting.string:
                meeting_log = "https://meetbot-raw.fedoraproject.org" + "/" + \
                              channel + "/" + datetxt + "/" + meeting.string
                meeting_sum = "https://meetbot-raw.fedoraproject.org" + "/" + \
                              channel + "/" + datetxt + "/" + meeting.string.replace(".log.html", ".html")
                meeting_key = meeting.string.replace(datetxt + "-", "").replace(".log.html", "")
                meeting_dict[meeting_key] = {
                    "logs": meeting_log,
                    "summary": meeting_sum
                }
        return True, meeting_dict
    except Exception as expt:
        return False, {"exception": str(expt)}


def fetch_meeting_logs_and_summary(meetname: str, summlink: str, logslink: str):
    try:
        summary_markup = ulrq.urlopen(ulpr.quote(summlink, safe=":/")).read().decode()
        logs_markup = ulrq.urlopen(ulpr.quote(logslink, safe=":/")).read().decode()
        textitem_dict = {
            "meetname": meetname,
            "summary_markup": summary_markup,
            "logs_markup": logs_markup
        }
        return True, textitem_dict
    except Exception as expt:
        return False, {"exception": str(expt)}


if __name__ == "__main__":
    print(fetch_channel_dict())
    print(fetch_datetxt_dict("allegheny"))
    print(fetch_meeting_dict("allegheny", "2010-04-08"))