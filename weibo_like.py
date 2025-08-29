import os
import sys
import time
from typing import List, Dict

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


def parse_cookie_header(cookie_header: str, domain: str) -> List[Dict]:
	"""Convert a Cookie header string into Playwright cookie dicts for a given domain."""
	cookies: List[Dict] = []
	if not cookie_header:
		return cookies
	for part in cookie_header.split(";"):
		if "=" not in part:
			continue
		name, value = part.split("=", 1)
		name = name.strip()
		value = value.strip()
		if not name:
			continue
		cookies.append({
			"name": name,
			"value": value,
			"domain": domain,
			"path": "/",
			"httpOnly": False,
			"secure": True,
		})
	return cookies


def add_weibo_cookies(context, cookie_header: str) -> None:
	"""Add cookies for common Weibo domains if provided."""
	if not cookie_header:
		return
	domains = [
		".weibo.com",
		"weibo.com",
		".s.weibo.com",
		"s.weibo.com",
		".m.weibo.cn",
		"m.weibo.cn",
	]
	all_cookies: List[Dict] = []
	for domain in domains:
		all_cookies.extend(parse_cookie_header(cookie_header, domain))
	if all_cookies:
		context.add_cookies(all_cookies)


def open_first_hot_search_and_like() -> int:
	weibo_cookie = os.environ.get("WEIBO_COOKIE", "").strip()
	trending_urls = [
		"https://s.weibo.com/top/summary?cate=realtimehot",
		"https://s.weibo.com/top/summary",
	]

	def debug_dump(page, name: str) -> None:
		try:
			png_path = f"/workspace/weibo_{name}.png"
			html_path = f"/workspace/weibo_{name}.html"
			page.screenshot(path=png_path, full_page=True)
			with open(html_path, "w", encoding="utf-8") as f:
				f.write(page.content())
			print(f"Saved debug snapshot: {png_path}, {html_path}")
		except Exception as e:
			print(f"Failed to save debug snapshot for {name}: {e}")

	with sync_playwright() as p:
		browser = p.chromium.launch(headless=True)
		context = browser.new_context(
			viewport={"width": 1280, "height": 800},
			user_agent=(
				"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
				"(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
			),
			locale="zh-CN",
			timezone_id="Asia/Shanghai",
		)
		add_weibo_cookies(context, weibo_cookie)
		page = context.new_page()

		first_link = None
		for url in trending_urls:
			print(f"Opening trending page: {url}")
			page.goto(url, wait_until="domcontentloaded", timeout=60000)
			time.sleep(2)
			try:
				page.wait_for_selector("td.td-02 a[href]", timeout=20000)
			except PlaywrightTimeoutError:
				debug_dump(page, "trending_timeout")
				continue

			candidate_selectors = [
				"table tbody tr td.td-02 a[href]",
				"#pl_top_realtimehot tbody tr td.td-02 a[href]",
				"a[href*='Refer=top']",
				"a[href^='/weibo?q=']",
			]

			for selector in candidate_selectors:
				locator = page.locator(selector)
				if locator.count() > 0:
					first_link = locator.first
					break

			if first_link:
				break

		if not first_link:
			print("Could not locate hot search list on the trending pages.")
			debug_dump(page, "trending_no_list")
			context.close(); browser.close()
			return 2

		try:
			first_topic_text = first_link.inner_text(timeout=15000)
		except PlaywrightTimeoutError:
			first_topic_text = "(unknown)"

		print(f"Clicking first hot search topic: {first_topic_text}")
		first_link.click(timeout=30000)
		page.wait_for_load_state("domcontentloaded", timeout=60000)
		time.sleep(2)
		debug_dump(page, "topic_page")

		# We are now on the topic/search results page. Attempt to like the first post.
		# We try several likely selectors for the like button.
		like_selectors = [
			"a[action-type='fl_like']",  # classic weibo selector
			"a[action-type='like']",
			"a[title*='赞']",
			"button:has-text('赞')",
			"span:has-text('赞')",
			"i:has-text('赞')",
			".card-act a:has-text('赞')",
			".woo-like-main",  # newer woo components
			".woo-like-ctrl",
		]

		like_clicked = False
		for selector in like_selectors:
			locator = page.locator(selector)
			if locator.count() > 0:
				try:
					locator.first.scroll_into_view_if_needed(timeout=10000)
					locator.first.click(timeout=15000)
					like_clicked = True
					break
				except Exception:
					continue

		if like_clicked:
			print("Attempted to click the like button on the first post.")
			status = 0
		else:
			print("Could not find a like button. You may need to be logged in.")
			debug_dump(page, "like_not_found")
			status = 3

		context.close(); browser.close()
		return status


if __name__ == "__main__":
	try:
		code = open_first_hot_search_and_like()
		sys.exit(code)
	except Exception as exc:
		print(f"Error: {exc}")
		sys.exit(1)

