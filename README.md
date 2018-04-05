Terminal emulators benchmarking suite
=====================================

This repository holds test scripts and results for a LWN article about
terminal emulators written in 2017-2018.

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-generate-toc again -->
**Table of Contents**

- [Terminal emulators benchmarking suite](#terminal-emulators-benchmarking-suite)
- [Methodology](#methodology)
- [Feature tests](#feature-tests)
    - [Unicode](#unicode)
    - [Paste protection](#paste-protection)
    - [Tabs and profiles](#tabs-and-profiles)
    - [Eye candy](#eye-candy)
    - [Original feature review](#original-feature-review)
- [Performance tests](#performance-tests)
- [Not evaluated](#not-evaluated)
- [Final notes](#final-notes)

<!-- markdown-toc end -->

Methodology
===========

Those tests were built over a period of 6 months, with variable
methodology for different tests. Two main family of tests were
performed: features and performance.

Unless otherwise noted, all tests were performed with the same
hardware (Intel i3-6100U CPU @ 2.30GHz, 16GiB DD4 RAM, Intel HD
Graphics 520 controller and 1680x1050 screen @ 59.95Hz). If
customization was performed on the terminal, a note was added in the
summary. Some terminals had to use a special font for the latency test
to work (e.g. using the then-standard `-font
'-adobe-courier-medium-r-normal--14-100-100-100-m-90-iso8859-1'`
argument), but were otherwise using the default font. A unicode locale
(either `fr_CA.UTF-8` or `en_US.UTF-8`) was used for all tests.

A battery of tests were done in July 17 on Debian 9.0, and tests were
redone in March 2018 on Debian 9.4 and Fedora 27.

| Terminal            | Debian        | Fedora  | Upstream | Notes                                      |
| ------------------- | ------------- | ------- | -------- | ------------------------------------------ |
| [Alacritty][]       | N/A           | N/A     | 6debc4f  | no releases Git head                       |
| [GNOME Terminal][]  | 3.22.2        | 3.26.2  | 3.28.0   | uses GTK3, [VTE][]                         |
| [Konsole][]         | 16.12.0       | 17.12.2 | 17.12.3  | uses KDE libraries                         |
| [mlterm][]          | 3.5.0         | 3.7.0   | 3.8.5    | uses VTE, "Multi-lingual terminal"         |
| [pterm][]           | 0.67          | 0.70    | 0.70     | [PuTTY][] without ssh, uses GTK2           |
| [st][]              | 0.6           | 0.7     | 0.8.1    | "simple terminal"                          |
| [Terminator][]      | 1.90+bzr-1705 | 1.91    | 1.91     | uses GTK3, VTE                             |
| [urxvt][]           | 9.22          | 9.22    | 9.22     | main rxvt fork, also known as rxvt-unicode |
| [Xfce Terminal][]   | 0.8.3         | 0.8.7   | 0.8.7.2  | uses GTK3, VTE                             |
| [xterm][]           | 327           | 330     | 331      | the original X terminal                    |

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
 [urxvt]: http://software.schmorp.de/pkg/rxvt-unicode.html
 [Xfce Terminal]: https://docs.xfce.org/apps/terminal/start
 [XTerm]: http://invisible-island.net/xterm/

Alacritty was only tested on Debian and doesn't have tagged releases
yet. The latest commit available at the time of writing was:

    commit 6debc4f3351446417d0c4e38173cd9ef0faa71d5
    Author: YOSHIOKA Takuma <lo48576@hard-wi.red>
    Date:   Tue Mar 13 20:16:01 2018 +0900

        Try to create window with different SRGB config when failed
        
        This may truly solve #921 (and issue caused by #1178)
        <https://github.com/jwilm/alacritty/issues/921#issuecomment-372619121>.

mlterm is not shipped with Fedora by default, so this [copr
repository](https://copr.fedorainfracloud.org/coprs/rabiny/mlterm/) was used as an alternative. Because it only supports
F26 out of the box, the `.repo` file was modified to hardcode the
version number:

    --- /etc/yum.repos.d/rabiny-mlterm.repo.orig	2018-03-28 17:06:43.048093670 -0400
    +++ /etc/yum.repos.d/rabiny-mlterm.repo	2018-03-28 17:06:19.671757651 -0400
    @@ -1,6 +1,6 @@
     [rabiny-mlterm]
     name=Copr repo for mlterm owned by rabiny
    -baseurl=https://copr-be.cloud.fedoraproject.org/results/rabiny/mlterm/fedora-$releasever-$basearch/
    +baseurl=https://copr-be.cloud.fedoraproject.org/results/rabiny/mlterm/fedora-26-$basearch/
     type=rpm-md
     skip_if_unavailable=True
     gpgcheck=1

Feature tests
=============

Those results cover the first part of the series, the features.

Unicode
-------

Unicode rendering tests were performed in a Debian Stretch 9.4
virtual machine, using the following procedure:

    vagrant up debian/stretch64
    vagrant ssh -c "sudo apt install xorg xterm rxvt-unicode mlterm kterm gnome-terminal blackbox"
    vagrant ssh -c "echo 'w6ksIM6ULCDQmSwg16cgLNmFLCDguZcsIOOBgizlj7YsIOiRiSwgYW5kIOunkAo=' | base64 -d > magicstring"

Then start VirtualBox, login (vagrant/vagrant) and start a GUI:

    xinit blackbox

Tests were also performed on a clean, on-disk Fedora 27 install.

Once a GUI is available, start the terminal and cat the magic file:

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

As a reference, the two test strings display up correctly in Emacs 25
on Fedora 27 and Debian 9. The two strings should look like this:

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

Note that the word "sarah" is surrounded by newlines otherwise it does
not show up correctly in Emacs, which directions are per paragraph,
not per line. Also note that Firefox displays the first string
correctly, but fails to align the sarah string to right. I will not
try to lose myself in the mists to figure out why this happens: if
anything, it could be that browsers do this per DOM block or for the
whole document.

Here are the results of a test performed on Debian 9 and verified on
Fedora 27:

| Terminal            | All | Order | From right |
| ------------------- | --- | ----  | ---------- |
| [Alacritty][]       |  ✓  |  x    |     x      |
| [GNOME Terminal][]  |  ✓  |  x    |     x      |
| [Konsole][]         |  ✓  |  ✓    |     x      |
| [mlterm][]          |  ✓¹ |  ✓    |     ✓      |
| [pterm][]           |  ✓  |  ✓    |     ✓      |
| [urxvt][]           |  ✓  |  x    |     x      |
| [st][]              |  ✓  |  x    |     x      |
| [Terminator][]      |  ✓  |  x    |     x      |
| [Xfce Terminal][]   |  ✓  |  x    |     x      |
| [xterm][]           |  x  |  x    |     x      |

¹ mlterm 3.5, as packaged in Debian, does not render all characters
properly, most of them being rendered as boxes:

![mlterm 3.5 in Debian not rendering characters correctly](unicode-mlterm-3.5-fail.png)

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

| Terminal            | without  | with, 2nd box |
| ------------------- | -------- | ------------- |
| [Alacritty][]       |  x       |       x       |
| [GNOME Terminal][]  |  x       |       ✓       |
| [Konsole][]         |  x       |       x       |
| [mlterm][]          |  x       |       x       |
| [pterm][]           |  x       |       x       |
| [st][]              |  x       |       x       |
| [Terminator][]      |  x       |       ✓       |
| [urxvt][]           |  x       |       x       |
| urxvt+confirm-paste |  ✓       |       ✓       |
| [Xfce Terminal][]   |  x       |       ✓       |
| [xterm][]           |  x       |       ✓       |

 * without: test results without a `.inputrc` configured, same in the
   two boxes
 * with, 2nd box: test with a `.inputrc`, but with the second box
   (first box always succeeds in all tested terminals)

The test succeeds if the commands are *not* ran.

The magic `.inputrc` line is:

	set enable-bracketed-paste on

This was tested on Debian 9 and Fedora 27.

Tabs and profiles
-----------------

| Terminal            | Tabs | Profiles | Linked |
| ------------------- | ---- | -------- | ------ |
| [Alacritty][]       |  x   |    x     |  N/A   |
| [GNOME Terminal][]  |  ✓   |    ✓     |   ✓    |
| [Konsole][]         |  ✓   |    ✓     |   ✓    |
| [mlterm][]          |  x   |    x     |  N/A   |
| [pterm][]           |  x   |    x     |  N/A   |
| [st][]              |  x   |    x     |  N/A   |
| [Terminator][]      |  ✓   |    ✓     |   x³   |
| [urxvt][]           |  ✓²  |    x     |   x    |
| [Xfce Terminal][]   |  ✓   |    x     |  N/A   |
| [xterm][]           |  x   |    x     |  N/A   |

² urxvt supports tabs through a plugin.

³ I couldn't figure out how to start a given profile in a given
Terminator tab.

 * Tabs: display and manage multiple tabs (`!` means through a plugin)
 * Profiles: if custom settings or command can be retained in
   different profiles
 * Linked: if specific tabs can be made to start a specific profile
   out of the box. not applicable (N/A) for terminals without profile
   support, obviously.

This was verified by clicking around the terminal's GUI and looking at
documentation, first on Debian 9 and then confirmed on Fedora 27.

Eye candy
---------

This is more of a qualitative evaluation. This was done by inspecting
the visible menus in the application and some reference manuals.

| Terminal            | backgrounds | transparency | true-color | URL | text-wrap | scrollback |
| ------------------- | ----------- | ------------ | ---------- | --- | --------- | ---------- |
| [Alacritty][]       |     x       |      x       |     ✓      |  x  |    x      |      x     |
| [GNOME Terminal][]  |     ✓       |      ✓       |     ✓      |  ✓  |    ✓      |      ✓     |
| [Konsole][]         |     x       |      x       |     ✓      |  ✓  |    x      |      ✓     |
| [mlterm][]          |     ✓       |      ✓       |     ✓⁴     |  x  |    x      |      ✓     |
| [pterm][]           |     x       |      x       |     x      |  x  |    x      |      ✓     |
| [st][]              |     x       |      x       |     ✓      |  x  |    x      |      x     |
| [Terminator][]      |     x       |      ✓       |     ✓      |  ✓  |    ✓      |      ✓     |
| [urxvt][]           |     ✓       |      ✓       |     x      |  ✓  |    ✓      |      ✓     |
| [Xfce Terminal][]   |     ✓       |      ✓       |     ✓      |  ✓  |    ✓      |      ✓     |
| [xterm][]           |     x       |      x       |     x      |  x  |    x      |      ✓     |

⁴ mlterm fails the true-color test in Debian but succeeds in F27.

 * Backgrounds: if arbitrary images can be set in the background
 * Transparency: if we can see under the windows
 * True-color: does the terminal display more than 256 colors?
 * URL: detect URLs and make them clickable or activate with a
   keybinding
 * text-wrap: properly reflow long lines instead of trimming or
   stripping them
 * Scrollback: if screen history is preserved

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

All tests were done on Debian 9 and verified Fedora 27.

Original feature review
-----------------------

This is a more elaborate table of tests performed on Debian 9 in July,
but not validated on later versions with Fedora 27.

| Terminal   | backgrounds | transparency | freetype | true-color | profiles | scripting | daemon | tab | URL | paste | text-wrap | scrollback | unicode | version         |
| ---------- | ----------- | ------------ | -------- | ---------- | -------- | --------- | ------ | --- | --- | ----- | --------- | ---------- | ------- | --------------- |
| alacritty  |             |              |    ✓     |     ✓      |          |           |        |     |     |       |           |            |    ✓    | 3df394d         |
| gnome      |     ✓       |      ✓       |    ✓     |     ✓      |    ✓     |           |        |  ✓  |  ✓  |       |    ✓      |      ✓     |    ✓    | 3.22.2-1        |
| konsole    |             |              |    ✓     |     ✓      |    ✓     |     ✓     |        |  ✓  |  ✓  |       |           |      ✓     |    ✓    | 4:16.12.0-4     |
| kterm      |             |              |          |            |          |           |        |     |     |       |           |      ✓     |         | 6.2.0-46.2      |
| mlterm     |     ✓       |      ✓       |    ✓     |            |    ?     |     ?     |    ✓   |     |     |       |           |      ✓     |         | 3.5.0-1+b2      |
| mrxvt      |     ✓       |      ✓       |          |            |    ✓     |           |        |  ✓  |     |       |           |      ✓     |         | 0.5.4-2         |
| pterm      |             |              |    ✓     |            |    ✓     |           |        |     |     |       |           |      ✓     |    ✓    | 0.67-3          |
| st         |             |              |    ✓     |     ✓      |          |           |        |     |     |       |           |            |    ✓    | 0.6-1           |
| terminator |             |      ✓       |    ✓     |     ✓      |    ✓     |           |    ✓   | ✓   | ✓   |       |    ✓      |      ✓     |    ✓    | 1.90+bzr-1705-1 |
| urxvt      |     ✓       |      ✓       |    ✓     |            |          |     ✓     |    ✓   |     |  ✓  |   ✓   |    ✓      |      ✓     |    ✓    | 9.22-1+b1       |
| xfce       |     ✓       |      ✓       |    ✓     |     ✓      |          |           |        |  ✓  |  ✓  |       |    ✓      |      ✓     |    ✓    | 0.8.3-1         |
| xterm      |             |              |    ✓     |            |          |           |        |     |     |       |           |      ✓     |         | 327-2           |

What follows is a very rough/early draft of the first part of the
series giving a qualitative review of each terminal emulator.

### alacritty ###

Alphabetical order forces me to start with an apology: I have
added [alacritty](https://github.com/jwilm/alacritty) to this list even though it is not
actually [packaged in Debian](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=851639). It seemed to me it had a novel
approach of using GPU acceleration that merited further
inspection. Like other projects, its focus is not on features (it
doesn't even have a scrollback buffer!) but on performance. It does
feature excellent unicode and color support, but unfortunately fails
the line-wrapping and bracketed paste tests.

Compiling alacritty was a little bit of a challenge. I wanted to avoid
using [rustup.sh](https://rustup.rs/) because I do not endorse sites telling users to
blindly run `curl | sh` commandlines. Instead, I installed alacritty
using the following sequence:

    sudo apt install -t unstable rustc # need 1.15 or later
    sudo apt install cargo cmake libfreetype6-dev libfontconfig1-dev xclip
    git clone https://github.com/jwilm/alacritty && cd alacritty
    cargo build --release

Since there are no public releases of alacritty, this ended up testing
the 08b5ae52c1c7dc3587ad31eee3036b58c3df394d git version.

### Eterm ###

[Eterm](http://www.eterm.org/) was the default emulator for the [Englightenment][] desktop
environment, a long time ago. It is derived from rxvt and is designed
as a "feature rich replacement for xterm", which also shows a bit of
its age. Its unicode support is poor: only the latin1 character is
displayed properly, and it has trouble displaying a simple sudo prompt
in the test locale. It is unclear if freetype fonts are supported as
the font choices are limited to "font 1, 2, 3 and 4"...

 [Enlightenment]: https://en.wikipedia.org/wiki/Enlightenment_(software)

### gnome-terminal ###

[GNOME terminal](https://en.wikipedia.org/wiki/GNOME_Terminal) is the default terminal emulator shipped with
the [GNOME desktop environment](https://en.wikipedia.org/wiki/GNOME). gnome-terminal supports tabs, URL
detection, text-wrapping, customizable backgrounds, freetype fonts and
multiple profiles. gnome-terminal claims to have several
"compatibility features" but, in my experience, it sometimes struggles
to display exotic escape sequences. I had, in particular, trouble
operating menus on the serial console of a HP ProCurve switch, for
which I had to revert to xterm.

gnome-terminal is, like many other terminals evaluated here, based on
the [libvte](https://wiki.gnome.org/Apps/Terminal/VTE) library which handles the basic terminal emulation
features, and so will act as a poster child for the other emulators
derived from that library.

### konsole ###

[konsole](https://konsole.kde.org/) is the default terminal emulator of the KDE desktop
environment. Using libvte brings it good unicode support but it
doesn't have as good line-wrap support as gnome-terminal: expanding a
window doesn't flow the lines back again. Like gnome-terminal, it also
features profile support but also includes interesting features like
bookmarks and activity / silence notifications.

### kterm ###

[kterm](https://ja.wikipedia.org/wiki/Kterm), also known as "Kagotani term" (not to be confused with
the [kindle terminale emulator](https://github.com/bfabiszewski/kterm)) is another old terminal emulator
derived from xterm to enable multiple language support, especially
japanese. It fails the unicode test, but that may be because of
limitations in the default "fixed" font chosen by the terminal.

The custom font was used for the latency test.

### mlterm ###

[mlterm](http://mlterm.sourceforge.net/) is one of the only terminals supporting right-to-left
languages. It supports a graphical preferences dialog where features
like input methods, background image or transparency can be set. The
dialog also features a crude [scp](https://en.wikipedia.org/wiki/Secure_copy) client. It failed to unicode
test because the asian characters were displayed as boxes, probably an
issue with the default font chosen.

### mrxvt ###

[mrxvt](https://en.wikipedia.org/wiki/Mrxvt) is a fork of rxvt from 2004 that aims to provide multiple
tabs support. It claims multi-language support, but unicode support is
actually not implemented and it had trouble displaying a simple sudo
prompt in the test locale. Profiles are implemented, in a way, by
having custom commands per tab.

The custom font was used for the latency test.

### pterm ###

pterm is the terminal emulator of the famous [putty](https://www.chiark.greenend.org.uk/~sgtatham/putty/) ssh client,
mostly designed for the Windows operating system, but also ported to
UNIX. It has excellent unicode support and has a graphical preferences
dialog, but fails the true-color test and is otherwise generally
limited in terms of feature.

A custom font (Courier 12) was used for the latency test.

### rxvt-unicode ###

[rxvt-unicode](http://software.schmorp.de/pkg/rxvt-unicode.html) "is a fork of the well known terminal
emulator [rxvt](https://en.wikipedia.org/wiki/Rxvt)" (acronym for ou*r* e*x*tended *v*irtual
*t*erminal), designed as a simplified version
of [xterm](https://en.wikipedia.org/wiki/Xterm). rxvt-unicode naturally supports unicode but also adds a
significant number of features over the base rxvt terminal:

 * daemon mode: improves startup time and memory usage
 * embeded perl customization, which allows for:
   * tab support
   * regex scrollback searches
   * popup menus
   * URL detection
   * copy-paste injection protection
 * improved line-wrap support
 * freetype font support

rxvt-unicode claims to have an "improved and corrected terminfo", but
in reality, certain key escapes do not work really reliably across
operating systems. For example, "control-left" and "control-right"
skip words correctly on a urxvt terminal, but when you start a screen
session, those keybindings stop working. gnome-terminal and xterm do
not show the same behavior.

I have some customization in rxvt which may have affected the early
tests, including:

 * scrollbar disabled (`URxvt*scrollBar: False`)
 * 10 000 lines scrollback buffer (`URxvt*saveLines: 10000`)
 * plugins: URL matching and paste protection (`URxvt.perl-ext-common:
   default,matcher,confirm-paste`)

As you can see, rxvt-unicode is my primary terminal and that may bias
the results and conclusions shown in this article. I would argue it
would be difficult for any seasoned UNIX operator to *not* be biased
in writing such an article, unfortunately.

### st ###

[st](http://st.suckless.org/) or "simple terminal", is the (very) basic terminal emulator
from the [suckless tools](http://suckless.org/) project. It features excellent unicode
and color support, but doesn't have a scrollback buffer at all,
claiming that is the task of a terminal multiplexer like tmux or
screen. It doesn't, unfortunately, handle line wrapping very well.

### terminator ###

[terminator](https://gnometerminator.blogspot.ca/) is another terminal emulator based on libvte which
brings the usual excellent unicode and color support, but adds
interesting features like typing to multiple terminals and tiling
tabs.

### xfce4-terminal ###

Like gnome-terminal, XFCE's terminal default terminal emulator has
excellent unicode and color support thanks to the libvte backend. It
makes up for the lack of profile support by supporting background
images and transparency out of the box.

### xterm ###

[xterm](https://en.wikipedia.org/wiki/Xterm) is the "standard terminal emulator" for the X Window
System. It's one of the oldest terminal emulators out there, written
in 1984 when the work on X started.

Xterm has obscure features like [Tektronix](https://en.wikipedia.org/wiki/Tektronix_4010) emulation, which allows
to display graphics in the terminal. Unicode support is provided by a
separate binary, `uxterm`. xterm has support for "bracketed paste",
but fails the advanced Jann Horn test. Otherwise, Xterm's feature set
is fairly limited by modern standards: it has only 256 colors support,
the background color can be changed, but no transparency or background
image support.

I had a slightly customized xterm configuration:

 * font changed to Monospace Regular (freetype font)
 * scrollback history of 6 000 lines

### xvt ###

xvt is yet another xterm derivatives that aims to remove the extra
features of xterm. It seems like a mostly abandoned project: I
couldn't find a home page and the only reason it's mentioned here is
because it is available in Debian. It hasn't seen an upstream update
in Debian as far back as 2006, according to the [snapshot archive](http://snapshot.debian.org/package/xvt/),
which makes it pretty old indeed.

The custom font was used for the latency test.

Performance tests
=================

Those tests are for the second article in the series and will be
published later.

Not evaluated
=============

Terminals were selected based on their availability in Debian stretch
at first, and then only if they had an active upstream. Alacritty is
an exception to this, as the poster child for GPU-optimized terminals
built with trendy new programming languages (Rust, in this case).

Here is a non-exhaustive list of terminals that were explicitly
excluded from this review with some extra reasons when relevant:

 * dead upstream:
   * [aterm](http://www.afterstep.org/aterm.php): obsolete rxvt fork, for Afterstep
   * [eterm](https://tracker.debian.org/pkg/eterm): inactive rxvt fork, for Enlightenment
   * [kterm](https://ja.wikipedia.org/wiki/Kterm): Kagotani term, xterm fork for Japanese
   * [mrxvt](https://code.google.com/archive/p/mrxvt/): multi-tab rxvt fork
   * [multi-aterm](https://www.nongnu.org/materm/materm.html): fork of aterm, removed from Debian in 2010
   * [Multi GNOME Terminal](http://multignometerm.sourceforge.net/): largely superseded by GNOME Terminal,
     abandoned upstream, removed from Debian in 2008
   * [wterm](https://tracker.debian.org/pkg/wterm): abandoned rxvt fork, for Window Maker, not to be
     confused with the Wayland rewrite of st (see below)
   * [xiterm+thai](https://linux.thai.net/projects/xiterm+thai/): inactive fork of (x)iterm, which is itself an
     inactive (removed from Debian in 2010) fork of aterm
   * [xvt](https://tracker.debian.org/pkg/xvt): ancestor of rxvt, mostly inactive
 * not in Debian stable (might overlap with the above of course):
   * [cool-retro-term](https://github.com/Swordfish90/cool-retro-term)
   * [cxterm](https://tracker.debian.org/pkg/cxterm): last seen in Debian in 2002, althouh upstream looked
     [alive in 2011](http://cxterm.sourceforge.net/)
   * [evilvte](http://www.calno.com/evilvte/): removed in Debian in 2017
   * [germinal](https://www.imagination-land.org/tags/germinal.html)
   * [kitty](https://github.com/kovidgoyal/kitty): same approach as Alacritty
   * hanterm: last seen in Debian potato, can we stop now?
   * [osso-xterm](http://maemo.org/development/tools/doc/diablo/osso-xterm/): Maemo terminal, vte-based
   * [roxterm](http://roxterm.sourceforge.net/): removed from Debian in 2016, vte-based
   * [stjerm](https://code.google.com/archive/p/stjerm-terminal-emulator/) (yes, it's st-jerm, go figure: drop-down, gtk, etc.
   * [Terminology](https://www.enlightenment.org/about-terminology.md): also seems to have [serious stability
     issues](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=848370) and backporting is hard because of the E17 dependency
   * [tinyterm](https://code.google.com/archive/p/tinyterm/)
   * [wterm](https://github.com/majestrate/wterm): Wayland rewrite of st
 * too similar to other stuff:
   * all the GNOME terminal forks (MATE, [LXTerminal](http://wiki.lxde.org/en/LXTerminal), Cinnamon,
     etc)
   * [lilyterm](http://lilyterm.luna.com.tw/): "Very light and easy to use X Terminal Emulator",
     vte-based
   * [QTerminal](https://github.com/qterminal/qterminal)
   * [sakura](http://www.pleyades.net/david/projects/sakura): another vte-derivative
   * [termit](https://github.com/nonstop/termit): yet another vte terminal, with Lua scripting
   * [termite](https://github.com/thestinger/termite): another vte
   * [tilix](https://tracker.debian.org/pkg/tilix): vte-based tiling term
 * drop-down terminals went under my radar:
   * [guake](http://guake-project.org/): drop-down terminal for GNOME
   * [tilda](https://github.com/lanoxx/tilda): "Gtk based drop down terminal"
   * [Yakuake](https://yakuake.kde.org/): Konsole-based
 * were too big or hard to install
   * [Gate One](https://github.com/liftoff/GateOne)
   * [anyterm](https://anyterm.org/)
   * [domterm](https://domterm.org/)
   * [hyper](https://github.com/zeit/hyper)
   * [shellinabox](https://github.com/shellinabox/shellinabox)
   * [terminus](https://github.com/Eugeny/terminus)
   * [upterm](https://github.com/railsware/upterm)
   * ... or any Electron/web apps: adding those to the benchmarks
     would require me to change the Y scale to be logarithmic, which
     would be silly

The Linux console itself wasn't directly tested, as it was too
difficult to instrument performance tests, which would have been
mostly meaningless, except for the bandwidth tests, which is the least
important.

A more exhaustive [list of terminal emulators](https://wiki.archlinux.org/index.php/List_of_applications#Terminal_emulators) is also available on
the Arch wiki.

See also [issue #1](https://github.com/anarcat/terms-benchmarks/issues/1) for a discussion about which terminals were
selected. Additions to the review are, of course, welcome if verified.

Final notes
===========

This would be hosted on GitLab, like my other repos, but they have
[trouble rendering the images here](https://gitlab.com/gitlab-org/gitlab-ce/issues/32784#note_63703633) so this will have to do.
