import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';
import {getConfig} from './config-helpers';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

// Get URL configuration from environment variables (with defaults for local dev)
const {url, baseUrl} = getConfig();

const config: Config = {
  title: 'Smart Humanoid',
  tagline: 'Build robots that understand the physical world',
  favicon: 'img/favicon.ico',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // URL configuration from environment variables (see config-helpers.ts)
  // Defaults: url='http://localhost:3000', baseUrl='/'
  // Override with: SITE_URL and BASE_URL environment variables
  url,
  baseUrl,

  // GitHub pages deployment config.
  organizationName: 'jamilurrahmanmuhammad', // GitHub org/user name
  projectName: 'smart-humanoid', // Repo name

  onBrokenLinks: 'throw',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/jamilurrahmanmuhammad/smart-humanoid/tree/main/',
        },
        blog: false, // Blog disabled per spec
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      defaultMode: 'dark',
      disableSwitch: true, // Dark theme only per spec
      respectPrefersColorScheme: false,
    },
    navbar: {
      title: 'Smart Humanoid',
      logo: {
        alt: 'Smart Humanoid Logo',
        src: 'img/logo.svg',
      },
      items: [
        // Learn Free - links to documentation
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Learn Free',
        },
        // Labs - disabled placeholder (Coming Soon)
        {
          type: 'html',
          position: 'left',
          value: '<span class="navbar__item navbar__link navbar__link--disabled" aria-label="Labs - Coming Soon" title="Coming Soon" aria-disabled="true">Labs</span>',
        },
        // Personalize - disabled placeholder (Coming Soon)
        {
          type: 'html',
          position: 'left',
          value: '<span class="navbar__item navbar__link navbar__link--disabled" aria-label="Personalize - Coming Soon" title="Coming Soon" aria-disabled="true">Personalize</span>',
        },
        // Search placeholder (visible placeholder until search is implemented)
        {
          type: 'html',
          position: 'right',
          value: '<div class="navbar__search-placeholder" aria-label="Search placeholder"><span class="search-icon">🔍</span><span class="search-text">Search</span></div>',
        },
        // GitHub repository link
        {
          href: 'https://github.com/jamilurrahmanmuhammad/smart-humanoid',
          label: 'GitHub',
          position: 'right',
          'aria-label': 'GitHub repository',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'Tutorial',
              to: '/docs/intro',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'Stack Overflow',
              href: 'https://stackoverflow.com/questions/tagged/docusaurus',
            },
            {
              label: 'Discord',
              href: 'https://discordapp.com/invite/docusaurus',
            },
            {
              label: 'X',
              href: 'https://x.com/docusaurus',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/jamilurrahmanmuhammad/smart-humanoid',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Smart Humanoid. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
