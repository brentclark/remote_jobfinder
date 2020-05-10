#!/usr/bin/env python3
import re
import argparse
import html
import feedparser
from rich.console import Console

URLS = {
    'remoteok':
        "https://remoteok.io/remote-sys-admin-jobs.rss",
    'stackrss':
        "https://stackoverflow.com/jobs/feed/?r=true&tl=sysadmin+linux",
    'weworkremotely':
        "https://weworkremotely.com/categories/remote-devops-sysadmin-jobs.rss",
    'remotebase':
        "http://api.remotebase.io/companies?is_hiring=true&hiring_regions=United%20States",
}

def rssfeedgrab(feed):
    console = Console()
    rss = feedparser.parse(feed)
    for post in rss.entries:
        date = "%d-%02d-%02d" % (post.published_parsed.tm_year,\
            post.published_parsed.tm_mon,\
            post.published_parsed.tm_mday)

        content = f"""
        \r[bold blue]posted date:[/bold blue] {date}
        \r[bold green]title:[/bold green] {post.title}
        \r[bold yellow]link:[/bold yellow] {post.link}
        """

        if 'company' in post:
            content += f"\r[bold red]company:[/bold red] {post.company}\n"
        elif 'author' in post:
            content += f"\r[bold red]company:[/bold red] {post.author}\n"
        elif 'title' in post:
            content += f"\r[bold red]company:[/bold red] {post.title.split(':')[0]}\n"

        # Description cleanup
        # i.e. sanitise all XML/HTML characters to ASCII etc.
        description = html.unescape(post.description)
        description = re.sub('<[^<]+?>', '', description)
        description = description.strip()
        description = description.replace("“", '"')
        description = description.replace("\"", '')
        description = description.replace("/“", ' ')
        content += f"\r[bold white]description:\n[/bold white]{description}"
        console.print(content)
        print('-' * 200)

def weworkremotely():
    """ stackoverflow """
    rssfeedgrab(URLS['weworkremotely'])

def stackrss():
    """ stackoverflow """
    rssfeedgrab(URLS['stackrss'])

def remoteok():
    """ remoteok """
    rssfeedgrab(URLS['remoteok'])

def main():
    """ main function for pylint """

    parser = argparse.ArgumentParser(description="Simple SysAdmin Job(s) parser of Stackoverflow, RemoteOk, Weworkremotely.")
    parser.add_argument("--remoteok", action='store_true', help="Sysadmin jobs from RemoteOk")
    parser.add_argument("--stackoverflow", action='store_true', help="Sysadmin jobs from Stackoverflow")
    parser.add_argument("--weworkremotely", action='store_true', help="Sysadmin jobs from Weworkremotely")
    args = parser.parse_args()

    if args.remoteok:
        remoteok()
    elif args.stackoverflow:
        stackrss()
    elif args.weworkremotely:
        weworkremotely()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
