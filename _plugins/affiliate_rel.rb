# 给 _data/affiliates.yml 里列出的合作/返利链接自动补上 rel="sponsored nofollow noopener"。
#
# 为什么放在插件里而不是逐条写进 Markdown：Google 的链接政策要求带佣金的链接必须标注，
# 漏一条就是一条风险；集中在这里改，新增联盟时只要往 affiliates.yml 加一行，正文、附录、
# 优惠合集页里的同一个链接会一起被覆盖到。披露提示与 GA 点击追踪读的也是同一份清单。
#
# post_render 阶段改的是渲染后的 HTML，所以 Markdown 链接、行内 HTML 链接、表格里的链接
# 都能处理。GitHub Pages 的经典构建不跑自定义插件，但本站由 .github/workflows/pages.yml
# 自己 `bundle exec jekyll build`，插件会正常生效。
module AffiliateRel
  REQUIRED = %w[sponsored nofollow noopener].freeze

  def self.matches(site)
    @matches ||= begin
      domains = (site.data['affiliates'] || {})['domains'] || []
      domains.map { |d| d['match'] }.compact.map(&:strip).reject(&:empty?)
    end
  end

  def self.affiliate?(href, matches)
    matches.any? { |m| href.include?(m) }
  end

  def self.rewrite(html, matches)
    return html if html.nil? || matches.empty?

    html.gsub(/<a\s+([^>]*?)\s*>/i) do |tag|
      attrs = Regexp.last_match(1)
      href = attrs[/href\s*=\s*"([^"]*)"/i, 1] || attrs[/href\s*=\s*'([^']*)'/i, 1]

      if href.nil? || !affiliate?(href, matches)
        tag
      elsif (existing = attrs[/rel\s*=\s*"([^"]*)"/i, 1])
        merged = (existing.split(/\s+/) | REQUIRED).join(' ')
        %(<a #{attrs.sub(/rel\s*=\s*"[^"]*"/i, %(rel="#{merged}"))}>)
      else
        %(<a #{attrs} rel="#{REQUIRED.join(' ')}">)
      end
    end
  end
end

Jekyll::Hooks.register [:documents, :pages], :post_render do |doc|
  doc.output = AffiliateRel.rewrite(doc.output, AffiliateRel.matches(doc.site))
end
