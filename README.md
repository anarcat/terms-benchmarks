Terminal emulators benchmarking suite
-------------------------------------

This repository holds test scripts and results for a LWN article about
terminal emulators written in 2017-2018.

This would be hosted on GitLab, like my other repos, but they have
[trouble rendering the images here](https://gitlab.com/gitlab-org/gitlab-ce/issues/32784#note_63703633) so this will have to do.

To interact with the notebook, you can use [mybinder.org](https://mybinder.org/v2/gh/anarcat/terms-benchmarks/master?filepath=benchmarks.ipynb).

| Terminal            | Debian        | Fedora  | Upstream | Notes                    |
| ------------------- | ------------- | ------- | -------- | ------------------------ |
| [Alacritty][]       | 3df394d       | N/A     | N/A      | No releases, git head    |
| [GNOME Terminal][]  | 3.22.2        | 3.26.2  | 3.28.0   | uses GTK3, [VTE][]       |
| [Konsole][]         | 16.12.0       | 17.12.2 | 17.12.3  | uses KDE libraries       |
| [mlterm][]          | 3.5.0         | 3.7.0   | 3.8.5    | uses VTE, "Multi-lingual terminal" |
| [pterm][]           | 0.67          | 0.70    | 0.70     | [PuTTY][] without ssh, uses GTK2 |
| [st][]              | 0.6           | 0.7     | 0.8.1    | "simple terminal"        |
| [Terminator][]      | 1.90+bzr-1705 | 1.91    | 1.91     | uses GTK3, VTE           |
| [rxvt-unicode][]    | 9.22          | 9.22    | 9.22     | Main rxvt fork           |
| [Xfce Terminal][]   | 0.8.3         | 0.8.7   | 0.8.7.2  | uses GTK3, VTE           |
| [xterm][]           | 327           | 330     | 331      | the original             |

 [Alacritty]: https://github.com/jwilm/alacritty
 [GNOME Terminal]: https://wiki.gnome.org/Apps/Terminal
 [Konsole]: https://konsole.kde.org/
 [kterm]: https://ja.wikipedia.org/wiki/Kterm
 [mlterm]: http://mlterm.sourceforge.net/
 [mrxvt]: https://en.wikipedia.org/wiki/Mrxvt
 [pterm]: https://manpages.debian.org/pterm
 [PuTTY]: https://www.chiark.greenend.org.uk/~sgtatham/putty/
 [st]: https://st.suckless.org/
 [Terminator]: https://gnometerminator.blogspot.ca/
 [VTE]: https://github.com/GNOME/vte
 [rxvt-unicode]: http://software.schmorp.de/pkg/rxvt-unicode.html
 [Xfce Terminal]: https://docs.xfce.org/apps/terminal/start
 [XTerm]: http://invisible-island.net/xterm/

Feature tests
=============

Those results cover the first part of the series, the features.

Unicode
-------

Unicode rendering tests were performed in a Debian Stretch 9.4.0
virtual machine, using the following procedure:

    vagrant up debian/stretch64
    vagrant ssh -c "sudo apt install xorg xterm rxvt-unicode mlterm kterm gnome-terminal blackbox"
    vagrant ssh -c "echo 'w6ksIM6ULCDQmSwg16cgLNmFLCDguZcsIOOBgizlj7YsIOiRiSwgYW5kIOunkAo=' | base64 -d > magicstring"

Then start VirtualBox, login (vagrant/vagrant) and start a GUI:

    xinit blackbox

In blackbox, start a terminal and cat the magic file:

    cat magicstring

The magic string was taken [from the Wikipedia Unicode page](https://en.wikipedia.org/wiki/Unicode#Web), with
a "é" added to make the string a little more familiar to western readers:

> For example, the references &#916;, &#1049;, &#1511;, &#1605;,
> &#3671;, &#12354;, &#21494;, &#33865;, and &#47568; (or the same
> numeric values expressed in hexadecimal, with &#x as the prefix)
> should display on all browsers as Δ, Й, ק ,م, ๗, あ, 叶, 葉, and 말.

In the magic string, all characters should be displayed properly, as
long as *one* font on the system supports the script, even if it's not
the font configured in the terminal. The Qoph and Mem characters
should also be display "backwards", that is "right-to-left: the mem
character should visually be displayed right after the Yot character
(`Й`) even if it's actually listed after Qoph.

Another magic string that was tested is the Hebrew name "Sarah"
(`שרה`, or `16nXqNeUCg==`), taken from the [bi-directional text
wikipedia page](https://en.wikipedia.org/wiki/Bi-directional_text):

> Many computer programs fail to display bi-directional text
> correctly. For example, the Hebrew name Sarah (שרה) is spelled: sin
> (ש) (which appears rightmost), then resh (ר), and finally heh (ה)
> (which should appear leftmost).

As a reference, the two test strings display up correctly in Firefox
57 and Emacs 25 on Fedora 27 and Debian 9. Those two programs are
considered to be correct implementations of this test. The two strings
should look like this:

![Magic string and Sarah in Hebrew correctly displayed by Emacs 25](magicstring-sarah.png)

To perform the test, the above two strings were stored in two distinct
files ([magicstring](magicstring) and [sarah](sarah)) and displayed, one at a time,
with two distinct `cat` commands:

```
[anarcat@curiehat terms-benchmarks]$ cat magicstring
é, Δ, Й, ק ,م, ๗, あ,叶, 葉, and 말
[anarcat@curiehat terms-benchmarks]$ cat sarah 
שרה
```

Here are some results performed on Fedora 27:

| Terminal            | All | Order | From right |
| ------------------- | --- | ----  | ---------- |
| [Alacritty][]       | N/A | N/A   | N/A |
| [GNOME Terminal][]  |  ✓  |  x    |  x  |
| [Konsole][]         |  ✓  |  ✓    |  x  |
| [mlterm][]          |  ✓  |  ✓    |  ✓  |
| [pterm][]           |  ✓  |  ✓    |  ✓  |
| [st][]              |  ✓  |  x    |  x  |
| [Terminator][]      |  ✓  |  x    |  x  |
| [rxvt-unicode][]    |  ✓  |  x    |  x  |
| [Xfce Terminal][]   |  ✓  |  x    |  x  |
| [xterm][]           |  x  |  x    |  x  |

Details:

 * All: all characters are properly displayed in the default configuration
 * Order: The "mem" and "qoph" characters are in the proper order
 * From right: the "Sara" word is display from the right margin

Paste protection
----------------

Here the test is to copy-paste the text in the first and second test
boxes from [Jann Horn's test site](http://thejh.net/misc/website-terminal-copy-paste). Text was copied using the
`CLIPBOARD` buffer (`control-c`, `control-v`) when possible, otherwise
the middle mouse button was used to copy the content of the
boxes. Here are the results, with and without the `.inputrc`
configuration in Bash:

|                   | No .inputrc | With .inputrc |
| Terminal            | 1st | 2nd | 1st | 2nd |
| ------------------- | --- | --- | --- | --- |
| [Alacritty][]       | N/A | N/A | N/A | N/A |
| [GNOME Terminal][]  |  x  |  x  |  ✓  |  ✓  |
| [Konsole][]         |  x  |  x  |  ✓  |  x  |
| [mlterm][]          |  x  |  x  |  ✓  |  x  |
| [pterm][]           |  x  |  x  |  ✓  |  x  |
| [st][]              |  x  |  x  |  ✓  |  x  |
| [Terminator][]      |  x  |  x  |  ✓  |  ✓  |
| [rxvt-unicode][]    |  x  |  x  |  ✓  |  x  |
| rxvt+confirm-paste  |  ✓  |  ✓  |  ✓  |  ✓  |
| [Xfce Terminal][]   |  x  |  x  |  ✓  |  ✓  |
| [xterm][]           |  x  |  x  |  ✓  |  ✓  |

The magic `.inputrc` line is:

	set enable-bracketed-paste on

This was tested on Debian 9 and Fedora 27.

Tabs and profiles
-----------------

| Terminal            | Tabs | Profiles | Linked |
| ------------------- | ---- | -------- | ------ | 
| [Alacritty][]       |   x  |   x | N/A |
| [G XME Terminal][]  |   ✓  |  ✓  |  ✓  |
| [Konsole][]         |  ✓  |  ✓  |  ✓  |
| [mlterm][]          |  x |  x | N/A |
| [pterm][]           |  x |  x | N/A |
| [st][]              |  x |  x | N/A |
| [Terminator][]      |  ✓  |  ✓  |  x |
| [rxvt-unicode][]    | plugin |  x |  x |
| [Xfce Terminal][]   |  ✓  |  x | N/A |
| [xterm][]           |  x |  x | N/A |

 * Tabs: if the terminal supports tabs ("plugin" means yes, through a plugin)
 * Profiles: if the terminal has a concept of profiles
 * Linked: if specific tabs can be made to start a specific profile out of the box.

I couldn't figure out how to start a given profile in a given
Terminator tab.

Eye candy
---------

This is more of a qualitative evaluation. This was done by inspecting
the visible menus in the application and some reference manuals.

| Terminal            | backgrounds | transparency | true-color | URL | text-wrap | scrollback |
| ------------------- | ----------- | ------------ | ---------- | --- | --------- | ---------- | 
| [Alacritty][]       |     x       |      x       |     ✓      |  x  |    x      |      x     | 
| [GNOME Terminal][]  |     ✓       |      ✓       |     ✓      |  ✓  |    ✓      |      ✓     | 
| [Konsole][]         |     x       |      x       |     ✓      |  ✓  |    x      |      ✓     | 
| [mlterm][]          |     ✓       |      ✓       |     ✓      |  x  |    x      |      ✓     | 
| [pterm][]           |     x       |      x       |     x      |  x  |    x      |      ✓     | 
| [st][]              |     x       |      x       |     ✓      |  x  |    x      |      x     | 
| [Terminator][]      |     x       |      ✓       |     ✓      |  ✓  |    ✓      |      ✓     | 
| [rxvt-unicode][]    |     ✓       |      ✓       |     x      |  ✓  |    ✓      |      ✓     | 
| [Xfce Terminal][]   |     ✓       |      ✓       |     ✓      |  ✓  |    ✓      |      ✓     | 
| [xterm][]           |     x       |      x       |     x      |  x  |    x      |      ✓     | 

 * Backgrounds: if arbitrary images can be set in the background
 * Transparency: if we can see under the windows
 * True-color: if more than 256 colors are supported. mlterm fails in Debian but succeeds in F27.
 * URL: if URLs are outlined and clickable
 * text-wrap: if long lines are properly reflowed
 * Scrollback: if there's a scrollback buffer at all

The true-color test was the following:

    awk 'BEGIN{
        s="/\\/\\/\\/\\/\\"; s=s s s s s s s s;
        for (colnum = 0; colnum<77; colnum++) {
            r = 255-(colnum*255/76);
            g = (colnum*510/76);
            b = (colnum*255/76);
            if (g>255) g = 510-g;
            printf "\033[48;2;%d;%d;%dm", r,g,b;
            printf "\033[38;2;%d;%d;%dm", 255-r,255-g,255-b;
            printf "%s\033[0m", substr(s,colnum+1,1);
        }
        printf "\n";
    }'

The text-wrap test consists of showing the `tail` of a file with long
lines, for example a logfile (e.g. `/var/log/messages` in Debian or
`/var/log/dnf.log` in Fedora), and resizing the windows. A successful
test will keep all characters as the window is resized, and reflow
long lines. A failure is, for example, when characters disappear when
a window is shrinked and expanded or when an expanded window doesn't
rejoin long lines previously broken up.

Unless otherwise noted, all tests were confirmed on Debian 9 and
Fedora 27.

Original feature review
-----------------------

| Terminal   | backgrounds | transparency | freetype | true-color | profiles | scripting | daemon | tab | URL | paste | text-wrap | scrollback | unicode | version         |
| ---------- | ----------- | ------------ | -------- | ---------- | -------- | --------- | ------ | --- | --- | ----- | --------- | ---------- | ------- | --------------- |
| alacritty  |             |              |    ✓     |     ✓      |          |           |        |     |     |       |           |            |    ✓    | 3df394d         |
| gnome      |     ✓       |      ✓       |    ✓     |     ✓      |    ✓     |           |        |  ✓  |  ✓  |       |    ✓      |      ✓     |    ✓    | 3.22.2-1        |
| konsole    |             |              |    ✓     |     ✓      |    ✓     |           |        |  ✓  |  ✓  |       |           |      ✓     |    ✓    | 4:16.12.0-4     |
| kterm      |             |              |          |            |          |           |        |     |     |       |           |      ✓     |         | 6.2.0-46.2      |
| mlterm     |     ✓       |      ✓       |    ✓     |            |    ?     |     ?     |    ✓   |     |     |       |           |      ✓     |         | 3.5.0-1+b2      |
| mrxvt      |     ✓       |      ✓       |          |            |    ✓     |           |        |  ✓  |     |       |           |      ✓     |         | 0.5.4-2         |
| pterm      |             |              |    ✓     |            |    ✓     |           |        |     |     |       |           |      ✓     |    ✓    | 0.67-3          |
| st         |             |              |    ✓     |     ✓      |          |           |        |     |     |       |           |            |    ✓    | 0.6-1           |
| terminator |             |      ✓       |    ✓     |     ✓      |    ✓     |           |    ✓   | ✓   | ✓   |       |    ✓      |      ✓     |    ✓    | 1.90+bzr-1705-1 |
| urxvt      |     ✓       |      ✓       |    ✓     |            |          |     ✓     |    ✓   |     |  ✓  |   ✓   |    ✓      |      ✓     |    ✓    | 9.22-1+b1       |
| xfce       |     ✓       |      ✓       |    ✓     |     ✓      |          |           |        |  ✓  |  ✓  |       |    ✓      |      ✓     |    ✓    | 0.8.3-1         |
| xterm      |             |              |    ✓     |            |          |           |        |     |     |       |           |      ✓     |         | 327-2           |

The above was a more elaborate table of tests performed on Debian 9,
but not validated on later versions with Fedora 27.

Performance tests
=================

Those tests are for the second article in the series.
