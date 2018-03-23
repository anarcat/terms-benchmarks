Terminal emulators benchmarking suite
=====================================

This repository holds test scripts and results for a LWN article about
terminal emulators written in 2017-2018.

Most interesting results are in [this iPython notebook](benchmarks.ipynb). To
interact with the notebook, you can use [mybinder.org](https://mybinder.org/v2/gh/anarcat/terms-benchmarks/master?filepath=benchmarks.ipynb) or download
this repository locally and open the notebook with:

    jupyter benchmarks.ipynb

Methodology
===========

Those tests were built over a period of 6 months, with variable
methodology for different tests. Two main family of tests were
performed: latency and resources tests. Latency tests aim at
evaluating the input latency of the terminals, and resources looks at
how much bandwidth can be dumped in the terminal, and how much CPU and
memory it uses.

Unless otherwise noted, all tests were performed in July 2017 using
Debian packages, on Debian stretch 9.0 amd64 with the same hardware
(Intel i3-6100U CPU @ 2.30GHz, 16GiB DD4 RAM, Intel HD Graphics 520
controller and 1680x1050 screen @ 59.95Hz). If customization was
performed on the terminal, a note was added in the summary. Some
terminals had to use a special font for the latency test to work
(e.g. using the then-standard `-font
'-adobe-courier-medium-r-normal--14-100-100-100-m-90-iso8859-1'`
argument), but were otherwise using the default font. The locale used
was `fr_CA.UTF-8` for all tests.

Unicode tests
-------------

Unicode rendering tests were performed in a Debian Stretch 9.4.0
virtual machine, using the following procedure:

    vagrant up debian/stretch64
    vagrant ssh -c "sudo apt install xorg xterm rxvt-unicode mlterm kterm gnome-terminal blackbox"
    vagrant ssh -c "echo 'w6ksIM6ULCDQmSwg16cgLNmFLCDguZcsIOOBgizlj7YsIOiRiSwgYW5kIOunkAo=' | base64 -d > magicstring"

Then start VirtualBox, login (vagrant/vagrant) and start a GUI:

    xinit blackbox

In blackbox, start a terminal and cat the magic file:

    cat magicstring

Latency tests
-------------

Those are a reroll of tests performed by Pavel Fatin in [Typing with
pleasure](https://pavelfatin.com/typing-with-pleasure/), but for terminals instead of text editors.

The following procedure was used:

 * installed [Typometer](https://pavelfatin.com/typometer/) 1.0 from the [binary releases](https://github.com/pavelfatin/typometer/releases/download/v1.0.0/typometer-1.0-bin.zip)
 * ran with `java -jar typometer-1.0.jar`
 * for each terminal:
   1. open terminal in new workspace
   2. switch to typometer workspace
   3. click benchmark
   4. switch back
   5. some font tweaks if typometer complains

The results were saved in the `latency.csv` file.

Some notes:

 * typometer wasn't configured in any special way: we used the default
   settings

 * ran a bunch of tests first by hand, then re-ran the whole list
   systematically

 * repeated test seem to give similar results within ~0.2ms margins
   (including stddev) except max values

 * some tests were made to verify that workrave, redshift and other
   apps do not seem to influence latency. they do not, whereas Fatin
   said they did in his experiments.

 * graphs sorted by average latency

About the graph types: I originally chose a scattered graph inspired
by [this technique](https://pavelfatin.com/typing-with-pleasure/#methodology), after using a [swarmplot](http://seaborn.pydata.org/generated/seaborn.swarmplot.html) but that actually
moves the dots to space them out, which gives a wrong impression. The
[stripplot](http://seaborn.pydata.org/generated/seaborn.stripplot.html) with a tuned jitter is better. Also experimented with a
[violinplot](http://seaborn.pydata.org/generated/seaborn.violinplot.html) to better show the averages but went back to swarmplot
after feedback from mxs: easier to read and the point is not to be
accurate as much as to show things. In the end, noticed that the
regular boxplot shows outliers in Seaborn, so decided to use that
more conventional approach instead.

I also contacted [Fatin on Twitter](https://twitter.com/pavelfatin/) (through a Direct Message) for
his R sources to avoid duplicating work, but failed to get a
response. He might have used this [jitter technique](http://zevross.com/blog/2014/05/05/unhide-hidden-data-using-jitter-in-the-r-package-ggplot2/) to get the
diffuse effect.

I have also mostly reproduced Fatin's results in the latency tests, as
is shown in the `editors.csv` file.

Resources
---------

 * first tests (`performance.csv` and `performance.py`, also in the
   notebook) were done with:
 
        time seq -f "the quick brown fox jumps over the lazy dog %g" 1000000

   qualitative results of those are also visible below.

 * the `times-100x100000.csv` file was generated with
   [replicate.sh](https://github.com/anarcat/terms-benchmarks/blob/master/replicate.sh), which starts each terminal with the above
   benchmark (but only 100,000 loops instead of a million, to shorten
   the test time). this series of tests was performed on the same
   computer, but on Debian stretch 9.4 in March 2018.

That number was chosen because our original loop (one million lines)
means xterm take 30 seconds per test so 100 tests take 40 minutes,
just for xterm. We shorten this by an order of magnitude: rxvt still
takes around 40ms and xterm takes 250ms. Printing a *single* line in
rxvt takes only a fraction of that time (9ms), similar to xterm
(10ms), which is small enough to be ignored in our tests, so we
consider that startup time to be negligible.

Ideally, that script would do a similar loop with a one-line test, and
substract the average, but that's getting complicated for probably no
gain.

Qualitative evaluation
======================

This is the result of manual tests, which were turned (by hand) into
`performance.csv`. Note that CPU and memory usage here represent the
[seq(1)](https://manpages.debian.org/seq) command, not the terminal itself, so they are irrelevant.

urxvt
-----

1.02user 1.64system 0:02.79elapsed 95%CPU (0avgtext+0avgdata 1824maxresident)k
0inputs+0outputs (0major+78minor)pagefaults 0swaps

clean display

gnome-termixnal
--------------

(libvte)

    1.01user 1.63system 0:06.90elapsed 38%CPU (0avgtext+0avgdata 1944maxresident)k
    0inputs+0outputs (0major+80minor)pagefaults 0swaps

clean display

xterm
-----

    1.23user 2.15system 0:26.05elapsed 13%CPU (0avgtext+0avgdata 1876maxresident)k
    0inputs+0outputs (0major+82minor)pagefaults 0swaps

lots of jitter in the display

xvt
---

    5.22user 7.16system 5:27.89elapsed 3%CPU (0avgtext+0avgdata 1804maxresident)k
    0inputs+0outputs (0major+77minor)pagefaults 0swaps

really, really slow. doesn't focus.

some display jitter

couldn't run the latency test ("could not detect reference pattern"),
success with this font:

    xvt -font '-adobe-courier-medium-r-normal--14-100-100-100-m-90-iso8859-1'

pterm (putty)
-------------

    1.25user 1.40system 0:18.67elapsed 14%CPU (0avgtext+0avgdata 1888maxresident)k
    0inputs+0outputs (0major+78minor)pagefaults 0swaps

only jitter on last line

had to switch font to Courier 12 (from fixed) for latency test to work
as well.

kterm
-----

    2.50user 4.58system 0:24.17elapsed 29%CPU (0avgtext+0avgdata 1820maxresident)k
    0inputs+0outputs (0major+77minor)pagefaults 0swaps

screen flashes a lot

also font problem, startup:

    kterm -font '-adobe-courier-medium-r-normal--14-100-100-100-m-90-iso8859-1'

mrxvt
-----

    1.13user 1.57system 0:02.71elapsed 99%CPU (0avgtext+0avgdata 2000maxresident)k
    0inputs+0outputs (0major+83minor)pagefaults 0swaps

no noticeable screen flashing, very fast, tabs.

also font problem:

    mrxvt -font '-adobe-courier-medium-r-normal--14-100-100-100-m-90-iso8859-1'

mlterm
------

    1.12user 1.68system 0:09.08elapsed 30%CPU (0avgtext+0avgdata 1984maxresident)k
    0inputs+0outputs (0major+82minor)pagefaults 0swaps

some jitter here and there

xfce4-terminal
--------------

    0.92user 1.72system 0:06.94elapsed 38%CPU (0avgtext+0avgdata 1884maxresident)k
    0inputs+0outputs (0major+80minor)pagefaults 0swaps

(libvte)

no jitter

eterm
-----

    1.22user 1.75system 0:55.65elapsed 5%CPU (0avgtext+0avgdata 1888maxresident)k
    0inputs+0outputs (0major+80minor)pagefaults 0swaps

no jitter, but slow

latency test completely failed with errors: "available line length too
short" and "cannot detect reference pattern". given up.

st
--

    1.04user 1.44system 0:03.15elapsed 79%CPU (0avgtext+0avgdata 1800maxresident)k
    0inputs+0outputs (0major+76minor)pagefaults 0swaps

some jitter on last line

alacritty
---------

    0.90user 1.60system 0:02.52elapsed 99%CPU (0avgtext+0avgdata 2000maxresident)k
    0inputs+0outputs (0major+81minor)pagefaults 0swaps

[not in debian](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=851639) so had to build from source. avoidied
[rustup.sh](https://rustup.rs/) because of bad security practices, instead used this:

    sudo apt install -t unstable rustc # need 1.15 or later
    sudo apt install cargo cmake libfreetype6-dev libfontconfig1-dev xclip
    git clone https://github.com/jwilm/alacritty && cd alacritty
    cargo build --release

uses wayland?

no releases, used 08b5ae52c1c7dc3587ad31eee3036b58c3df394d on Debian
stretch with rustc from unstable to run the first informal (and
latency) tests.

tried to rerun the tests, but rebuild of july code segfaults in
march. ended up pulling in new code for the formal resource tests
(6debc4f3351446417d0c4e38173cd9ef0faa71d5).

konsole
-------

    1.16user 1.40system 0:05.32elapsed 48%CPU (0avgtext+0avgdata 1880maxresident)k
    0inputs+0outputs (0major+83minor)pagefaults 0swaps

no jitter but display hangs ever other second - kind of cheats
performance tests because it doesn't display the whole lot.

right-click pops a menu instead of extending primary selection

Terminator
----------

    1.00user 1.84system 0:07.18elapsed 39%CPU (0avgtext+0avgdata 1984maxresident)k
    0inputs+0outputs (0major+82minor)pagefaults 0swaps

(libvte)

no visible jitter

Terminus
--------

    1.34user 2.31system 0:03.83elapsed 95%CPU (0avgtext+0avgdata 1944maxresident)k
    0inputs+0outputs (0major+96minor)pagefaults 0swaps

1.0.0alpha42

takes 1m53 (wall clock, so does not match the above). cannot be tested
like other terminals because it doesn't support `-e`. terminal
completely unresponsive during the test. seems to do weird things to
the primary selection in an emacs running in another workspace.

latency test said "timeout expired", catastrophic delays in the
provisional results:

    min: 61.8 | max: 611.6 | avg: 159.6 | SD: 135.7

starting then killing:

    0.77user 0.18system 0:05.46elapsed 17%CPU (0avgtext+0avgdata 107676maxresident)k
    0inputs+24outputs (0major+21109minor)pagefaults 0swaps

takes 100MB of ram! says this on startup:

    Host startup: 38ms

installed with the Debian package.

Not evaluated
=============

All terminals were tested on Debian Stretch with a UTF-8 locale, using
Debian packages. Alacritty is an exception to this, as the poster
child for GPU-optimized terminals built with trendy new programming
languages (Rust, in this case). Some terminals in Debian were excluded
from the review, mostly because:

 * dead upstream:
   * [aterm](http://www.afterstep.org/aterm.php): obsolete rxvt fork, for Afterstep
   * [eterm](https://tracker.debian.org/pkg/eterm): inactive rxvt fork, for Enlightenment
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
   * [hyper](https://github.com/zeit/hyper)
   * [shellinabox](https://github.com/shellinabox/shellinabox)
   * [terminus](https://github.com/Eugeny/terminus)
   * [upterm](https://github.com/railsware/upterm)
   * ... or any Electron/web apps: adding those to the benchmarks
     would require me to change the Y scale to be logarithmic, which
     would be silly

A more exhaustive [list of terminal emulators](https://wiki.archlinux.org/index.php/List_of_applications#Terminal_emulators) is also available on
the Arch wiki.

Final notes
===========

This would be hosted on GitLab, like my other repos, but they have
[trouble rendering the images here](https://gitlab.com/gitlab-org/gitlab-ce/issues/32784#note_63703633) so this will have to do.
