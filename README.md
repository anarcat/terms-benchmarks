Terminal emulators benchmarking suite
-------------------------------------

This repository holds test scripts and results for a LWN article about
terminal emulators written in 2017-2018.

This would be hosted on GitLab, like my other repos, but they have
[trouble rendering the images here](https://gitlab.com/gitlab-org/gitlab-ce/issues/32784#note_63703633) so this will have to do.

To interact with the notebook, you can use [mybinder.org](https://mybinder.org/v2/gh/anarcat/terms-benchmarks/master?filepath=benchmarks.ipynb).

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
57 and Emacs 25 on Fedora 27 and Debian 9. Those two distinct programs
are considered to be correct implementations of this test. Again, the
text should show like this:

```
Δ, Й, ק ,م, ๗, あ, 叶, 葉, and 말
שרה
```

Here are some results performed on Fedora 27:

| Terminal            | All | RTL |
| ------------------- | --- | --- |
| [Alacritty][]       | 
| [GNOME Terminal][]  | yes | no  |
| [Konsole][]         | yes | yes | 
| [mlterm][]          | 
| [pterm][]           | yes | yes |
| [st][]              | yes | no  |
| [Terminator][]      | yes | no  |
| [rxvt-unicode][]    | yes | no  |
| [Xfce Terminal][]   | yes | no  |
| [xterm][]           | no  | no  |
