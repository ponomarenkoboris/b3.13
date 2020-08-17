class Tag:
    def __init__(self, tag, is_single=False, klass=None, **kwargs):
        self.tag = tag
        self.text = ""
        self.attributes = {}

        self.is_single = is_single
        self.children = []

        if klass is not None:
            self.attributes["class"] = " ".join(klass)

        for k, v in kwargs.items():
            if "_" in k:
                k = k.replace("_", "-")
            self.attributes[k] = v

    def __enter__(self, *args, **kwargs):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __str__(self):
        attrs = []
        for k, v in self.attributes.items():
            attrs.append(f'{k}="{v}"')
        attrs = " ".join(attrs)

        if len(self.children) > 0:
            opening = f"<{self.tag} {attrs}>"
            if self.text:
                internal = f"{self.text}"
            else:
                internal = ""
            for child in self.children:
                internal += str(child)
                ending = f"</{self.tag}>"
            return opening + internal + ending
        else:
            if self.is_single:
                return f"<{self.tag} {attrs}"
            else:
                return f"<{self.tag} {attrs}>{self.text}</{self.tag}>"



class HTML:
    def __init__(self, output=None):
        self.output = output
        self.children = []
        
    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        if self.output is not None:
            with open(self.output, "w") as f:
                f.write(str(self))
        else:
            print(self)

    def __str__(self):
        html = "<html>\n"
        for child in self.children:
            html += str(child)
        html += "\n</html>"
        return html



class TopLevelTag:
    def __init__(self, tag, **kwargs):
        self.tag = tag
        self.children = []

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def __str__(self):
        html = f"<{self.tag}>\n"
        for child in self.children:
            html += str(child)
        html += f"\n</{self.tag}>"
        return html


if __name__ == "__main__":
    with HTML(output=None) as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head

        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

                with Tag("img", is_single=True, src="/icon.png") as img:
                    div += img

                body += div

            doc += body