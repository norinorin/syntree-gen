# syntree-gen
A constituency-based parse tree generator.

### Phrase markers
syntree-gen takes phrase markers as input. For example, the input `[S [N John] [VP [V hit] [NP [D the] [N ball.]]]]` will result in:
<p align="center">
    <img src="sample.png" width="400" alt="Sample image of the syntax tree generated by syntree-gen">
</p>

### Installing prerequisites and running
```bash
pip install -r requirements.txt
python -OOm src -h
```