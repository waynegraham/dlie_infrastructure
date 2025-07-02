# Makefile: slide deck generation via Pandoc

SLIDES_MD := docs/slides.md
SLIDES_PPTX := docs/slides.pptx

PANDOC := pandoc
PANDOC_FLAGS := -t pptx --standalone --resource-path=docs/images

# If a custom PowerPoint template is provided, use it for styling
REF_DOC := docs/reference.pptx
ifneq (,$(wildcard $(REF_DOC)))
PANDOC_FLAGS += --reference-doc=$(REF_DOC)
endif

.PHONY: pptx
pptx: $(SLIDES_PPTX)

$(SLIDES_PPTX): $(SLIDES_MD)
	$(PANDOC) $(SLIDES_MD) $(PANDOC_FLAGS) -o $(SLIDES_PPTX)