/* eslint-disable */

// @ts-nocheck

// noinspection JSUnusedGlobalSymbols

// This file was automatically generated by TanStack Router.
// You should NOT make any changes in this file as it will be overwritten.
// Additionally, you should also exclude this file from your linter and/or formatter to prevent it from being checked or modified.

// Import Routes

import { Route as rootRoute } from './routes/__root'
import { Route as PublicLayoutImport } from './routes/_publicLayout'
import { Route as LayoutImport } from './routes/_layout'
import { Route as PublicLayoutIndexImport } from './routes/_publicLayout/index'
import { Route as PublicLayoutThanksImport } from './routes/_publicLayout/thanks'
import { Route as PublicLayoutSignupImport } from './routes/_publicLayout/signup'
import { Route as PublicLayoutLoginImport } from './routes/_publicLayout/login'
import { Route as LayoutCollectionsIndexImport } from './routes/_layout/collections/index'
import { Route as LayoutCollectionsCollectionIdIndexImport } from './routes/_layout/collections/$collectionId/index'
import { Route as LayoutCollectionsCollectionIdStatsImport } from './routes/_layout/collections/$collectionId/stats'
import { Route as LayoutCollectionsCollectionIdPracticeImport } from './routes/_layout/collections/$collectionId/practice'
import { Route as LayoutCollectionsCollectionIdCardsNewImport } from './routes/_layout/collections/$collectionId/cards/new'
import { Route as LayoutCollectionsCollectionIdCardsCardIdImport } from './routes/_layout/collections/$collectionId/cards/$cardId'

// Create/Update Routes

const PublicLayoutRoute = PublicLayoutImport.update({
  id: '/_publicLayout',
  getParentRoute: () => rootRoute,
} as any)

const LayoutRoute = LayoutImport.update({
  id: '/_layout',
  getParentRoute: () => rootRoute,
} as any)

const PublicLayoutIndexRoute = PublicLayoutIndexImport.update({
  id: '/',
  path: '/',
  getParentRoute: () => PublicLayoutRoute,
} as any)

const PublicLayoutThanksRoute = PublicLayoutThanksImport.update({
  id: '/thanks',
  path: '/thanks',
  getParentRoute: () => PublicLayoutRoute,
} as any)

const PublicLayoutSignupRoute = PublicLayoutSignupImport.update({
  id: '/signup',
  path: '/signup',
  getParentRoute: () => PublicLayoutRoute,
} as any)

const PublicLayoutLoginRoute = PublicLayoutLoginImport.update({
  id: '/login',
  path: '/login',
  getParentRoute: () => PublicLayoutRoute,
} as any)

const LayoutCollectionsIndexRoute = LayoutCollectionsIndexImport.update({
  id: '/collections/',
  path: '/collections/',
  getParentRoute: () => LayoutRoute,
} as any)

const LayoutCollectionsCollectionIdIndexRoute =
  LayoutCollectionsCollectionIdIndexImport.update({
    id: '/collections/$collectionId/',
    path: '/collections/$collectionId/',
    getParentRoute: () => LayoutRoute,
  } as any)

const LayoutCollectionsCollectionIdStatsRoute =
  LayoutCollectionsCollectionIdStatsImport.update({
    id: '/collections/$collectionId/stats',
    path: '/collections/$collectionId/stats',
    getParentRoute: () => LayoutRoute,
  } as any)

const LayoutCollectionsCollectionIdPracticeRoute =
  LayoutCollectionsCollectionIdPracticeImport.update({
    id: '/collections/$collectionId/practice',
    path: '/collections/$collectionId/practice',
    getParentRoute: () => LayoutRoute,
  } as any)

const LayoutCollectionsCollectionIdCardsNewRoute =
  LayoutCollectionsCollectionIdCardsNewImport.update({
    id: '/collections/$collectionId/cards/new',
    path: '/collections/$collectionId/cards/new',
    getParentRoute: () => LayoutRoute,
  } as any)

const LayoutCollectionsCollectionIdCardsCardIdRoute =
  LayoutCollectionsCollectionIdCardsCardIdImport.update({
    id: '/collections/$collectionId/cards/$cardId',
    path: '/collections/$collectionId/cards/$cardId',
    getParentRoute: () => LayoutRoute,
  } as any)

// Populate the FileRoutesByPath interface

declare module '@tanstack/react-router' {
  interface FileRoutesByPath {
    '/_layout': {
      id: '/_layout'
      path: ''
      fullPath: ''
      preLoaderRoute: typeof LayoutImport
      parentRoute: typeof rootRoute
    }
    '/_publicLayout': {
      id: '/_publicLayout'
      path: ''
      fullPath: ''
      preLoaderRoute: typeof PublicLayoutImport
      parentRoute: typeof rootRoute
    }
    '/_publicLayout/login': {
      id: '/_publicLayout/login'
      path: '/login'
      fullPath: '/login'
      preLoaderRoute: typeof PublicLayoutLoginImport
      parentRoute: typeof PublicLayoutImport
    }
    '/_publicLayout/signup': {
      id: '/_publicLayout/signup'
      path: '/signup'
      fullPath: '/signup'
      preLoaderRoute: typeof PublicLayoutSignupImport
      parentRoute: typeof PublicLayoutImport
    }
    '/_publicLayout/thanks': {
      id: '/_publicLayout/thanks'
      path: '/thanks'
      fullPath: '/thanks'
      preLoaderRoute: typeof PublicLayoutThanksImport
      parentRoute: typeof PublicLayoutImport
    }
    '/_publicLayout/': {
      id: '/_publicLayout/'
      path: '/'
      fullPath: '/'
      preLoaderRoute: typeof PublicLayoutIndexImport
      parentRoute: typeof PublicLayoutImport
    }
    '/_layout/collections/': {
      id: '/_layout/collections/'
      path: '/collections'
      fullPath: '/collections'
      preLoaderRoute: typeof LayoutCollectionsIndexImport
      parentRoute: typeof LayoutImport
    }
    '/_layout/collections/$collectionId/practice': {
      id: '/_layout/collections/$collectionId/practice'
      path: '/collections/$collectionId/practice'
      fullPath: '/collections/$collectionId/practice'
      preLoaderRoute: typeof LayoutCollectionsCollectionIdPracticeImport
      parentRoute: typeof LayoutImport
    }
    '/_layout/collections/$collectionId/stats': {
      id: '/_layout/collections/$collectionId/stats'
      path: '/collections/$collectionId/stats'
      fullPath: '/collections/$collectionId/stats'
      preLoaderRoute: typeof LayoutCollectionsCollectionIdStatsImport
      parentRoute: typeof LayoutImport
    }
    '/_layout/collections/$collectionId/': {
      id: '/_layout/collections/$collectionId/'
      path: '/collections/$collectionId'
      fullPath: '/collections/$collectionId'
      preLoaderRoute: typeof LayoutCollectionsCollectionIdIndexImport
      parentRoute: typeof LayoutImport
    }
    '/_layout/collections/$collectionId/cards/$cardId': {
      id: '/_layout/collections/$collectionId/cards/$cardId'
      path: '/collections/$collectionId/cards/$cardId'
      fullPath: '/collections/$collectionId/cards/$cardId'
      preLoaderRoute: typeof LayoutCollectionsCollectionIdCardsCardIdImport
      parentRoute: typeof LayoutImport
    }
    '/_layout/collections/$collectionId/cards/new': {
      id: '/_layout/collections/$collectionId/cards/new'
      path: '/collections/$collectionId/cards/new'
      fullPath: '/collections/$collectionId/cards/new'
      preLoaderRoute: typeof LayoutCollectionsCollectionIdCardsNewImport
      parentRoute: typeof LayoutImport
    }
  }
}

// Create and export the route tree

interface LayoutRouteChildren {
  LayoutCollectionsIndexRoute: typeof LayoutCollectionsIndexRoute
  LayoutCollectionsCollectionIdPracticeRoute: typeof LayoutCollectionsCollectionIdPracticeRoute
  LayoutCollectionsCollectionIdStatsRoute: typeof LayoutCollectionsCollectionIdStatsRoute
  LayoutCollectionsCollectionIdIndexRoute: typeof LayoutCollectionsCollectionIdIndexRoute
  LayoutCollectionsCollectionIdCardsCardIdRoute: typeof LayoutCollectionsCollectionIdCardsCardIdRoute
  LayoutCollectionsCollectionIdCardsNewRoute: typeof LayoutCollectionsCollectionIdCardsNewRoute
}

const LayoutRouteChildren: LayoutRouteChildren = {
  LayoutCollectionsIndexRoute: LayoutCollectionsIndexRoute,
  LayoutCollectionsCollectionIdPracticeRoute:
    LayoutCollectionsCollectionIdPracticeRoute,
  LayoutCollectionsCollectionIdStatsRoute:
    LayoutCollectionsCollectionIdStatsRoute,
  LayoutCollectionsCollectionIdIndexRoute:
    LayoutCollectionsCollectionIdIndexRoute,
  LayoutCollectionsCollectionIdCardsCardIdRoute:
    LayoutCollectionsCollectionIdCardsCardIdRoute,
  LayoutCollectionsCollectionIdCardsNewRoute:
    LayoutCollectionsCollectionIdCardsNewRoute,
}

const LayoutRouteWithChildren =
  LayoutRoute._addFileChildren(LayoutRouteChildren)

interface PublicLayoutRouteChildren {
  PublicLayoutLoginRoute: typeof PublicLayoutLoginRoute
  PublicLayoutSignupRoute: typeof PublicLayoutSignupRoute
  PublicLayoutThanksRoute: typeof PublicLayoutThanksRoute
  PublicLayoutIndexRoute: typeof PublicLayoutIndexRoute
}

const PublicLayoutRouteChildren: PublicLayoutRouteChildren = {
  PublicLayoutLoginRoute: PublicLayoutLoginRoute,
  PublicLayoutSignupRoute: PublicLayoutSignupRoute,
  PublicLayoutThanksRoute: PublicLayoutThanksRoute,
  PublicLayoutIndexRoute: PublicLayoutIndexRoute,
}

const PublicLayoutRouteWithChildren = PublicLayoutRoute._addFileChildren(
  PublicLayoutRouteChildren,
)

export interface FileRoutesByFullPath {
  '': typeof PublicLayoutRouteWithChildren
  '/login': typeof PublicLayoutLoginRoute
  '/signup': typeof PublicLayoutSignupRoute
  '/thanks': typeof PublicLayoutThanksRoute
  '/': typeof PublicLayoutIndexRoute
  '/collections': typeof LayoutCollectionsIndexRoute
  '/collections/$collectionId/practice': typeof LayoutCollectionsCollectionIdPracticeRoute
  '/collections/$collectionId/stats': typeof LayoutCollectionsCollectionIdStatsRoute
  '/collections/$collectionId': typeof LayoutCollectionsCollectionIdIndexRoute
  '/collections/$collectionId/cards/$cardId': typeof LayoutCollectionsCollectionIdCardsCardIdRoute
  '/collections/$collectionId/cards/new': typeof LayoutCollectionsCollectionIdCardsNewRoute
}

export interface FileRoutesByTo {
  '': typeof LayoutRouteWithChildren
  '/login': typeof PublicLayoutLoginRoute
  '/signup': typeof PublicLayoutSignupRoute
  '/thanks': typeof PublicLayoutThanksRoute
  '/': typeof PublicLayoutIndexRoute
  '/collections': typeof LayoutCollectionsIndexRoute
  '/collections/$collectionId/practice': typeof LayoutCollectionsCollectionIdPracticeRoute
  '/collections/$collectionId/stats': typeof LayoutCollectionsCollectionIdStatsRoute
  '/collections/$collectionId': typeof LayoutCollectionsCollectionIdIndexRoute
  '/collections/$collectionId/cards/$cardId': typeof LayoutCollectionsCollectionIdCardsCardIdRoute
  '/collections/$collectionId/cards/new': typeof LayoutCollectionsCollectionIdCardsNewRoute
}

export interface FileRoutesById {
  __root__: typeof rootRoute
  '/_layout': typeof LayoutRouteWithChildren
  '/_publicLayout': typeof PublicLayoutRouteWithChildren
  '/_publicLayout/login': typeof PublicLayoutLoginRoute
  '/_publicLayout/signup': typeof PublicLayoutSignupRoute
  '/_publicLayout/thanks': typeof PublicLayoutThanksRoute
  '/_publicLayout/': typeof PublicLayoutIndexRoute
  '/_layout/collections/': typeof LayoutCollectionsIndexRoute
  '/_layout/collections/$collectionId/practice': typeof LayoutCollectionsCollectionIdPracticeRoute
  '/_layout/collections/$collectionId/stats': typeof LayoutCollectionsCollectionIdStatsRoute
  '/_layout/collections/$collectionId/': typeof LayoutCollectionsCollectionIdIndexRoute
  '/_layout/collections/$collectionId/cards/$cardId': typeof LayoutCollectionsCollectionIdCardsCardIdRoute
  '/_layout/collections/$collectionId/cards/new': typeof LayoutCollectionsCollectionIdCardsNewRoute
}

export interface FileRouteTypes {
  fileRoutesByFullPath: FileRoutesByFullPath
  fullPaths:
    | ''
    | '/login'
    | '/signup'
    | '/thanks'
    | '/'
    | '/collections'
    | '/collections/$collectionId/practice'
    | '/collections/$collectionId/stats'
    | '/collections/$collectionId'
    | '/collections/$collectionId/cards/$cardId'
    | '/collections/$collectionId/cards/new'
  fileRoutesByTo: FileRoutesByTo
  to:
    | ''
    | '/login'
    | '/signup'
    | '/thanks'
    | '/'
    | '/collections'
    | '/collections/$collectionId/practice'
    | '/collections/$collectionId/stats'
    | '/collections/$collectionId'
    | '/collections/$collectionId/cards/$cardId'
    | '/collections/$collectionId/cards/new'
  id:
    | '__root__'
    | '/_layout'
    | '/_publicLayout'
    | '/_publicLayout/login'
    | '/_publicLayout/signup'
    | '/_publicLayout/thanks'
    | '/_publicLayout/'
    | '/_layout/collections/'
    | '/_layout/collections/$collectionId/practice'
    | '/_layout/collections/$collectionId/stats'
    | '/_layout/collections/$collectionId/'
    | '/_layout/collections/$collectionId/cards/$cardId'
    | '/_layout/collections/$collectionId/cards/new'
  fileRoutesById: FileRoutesById
}

export interface RootRouteChildren {
  LayoutRoute: typeof LayoutRouteWithChildren
  PublicLayoutRoute: typeof PublicLayoutRouteWithChildren
}

const rootRouteChildren: RootRouteChildren = {
  LayoutRoute: LayoutRouteWithChildren,
  PublicLayoutRoute: PublicLayoutRouteWithChildren,
}

export const routeTree = rootRoute
  ._addFileChildren(rootRouteChildren)
  ._addFileTypes<FileRouteTypes>()

/* ROUTE_MANIFEST_START
{
  "routes": {
    "__root__": {
      "filePath": "__root.tsx",
      "children": [
        "/_layout",
        "/_publicLayout"
      ]
    },
    "/_layout": {
      "filePath": "_layout.tsx",
      "children": [
        "/_layout/collections/",
        "/_layout/collections/$collectionId/practice",
        "/_layout/collections/$collectionId/stats",
        "/_layout/collections/$collectionId/",
        "/_layout/collections/$collectionId/cards/$cardId",
        "/_layout/collections/$collectionId/cards/new"
      ]
    },
    "/_publicLayout": {
      "filePath": "_publicLayout.tsx",
      "children": [
        "/_publicLayout/login",
        "/_publicLayout/signup",
        "/_publicLayout/thanks",
        "/_publicLayout/"
      ]
    },
    "/_publicLayout/login": {
      "filePath": "_publicLayout/login.tsx",
      "parent": "/_publicLayout"
    },
    "/_publicLayout/signup": {
      "filePath": "_publicLayout/signup.tsx",
      "parent": "/_publicLayout"
    },
    "/_publicLayout/thanks": {
      "filePath": "_publicLayout/thanks.tsx",
      "parent": "/_publicLayout"
    },
    "/_publicLayout/": {
      "filePath": "_publicLayout/index.tsx",
      "parent": "/_publicLayout"
    },
    "/_layout/collections/": {
      "filePath": "_layout/collections/index.tsx",
      "parent": "/_layout"
    },
    "/_layout/collections/$collectionId/practice": {
      "filePath": "_layout/collections/$collectionId/practice.tsx",
      "parent": "/_layout"
    },
    "/_layout/collections/$collectionId/stats": {
      "filePath": "_layout/collections/$collectionId/stats.tsx",
      "parent": "/_layout"
    },
    "/_layout/collections/$collectionId/": {
      "filePath": "_layout/collections/$collectionId/index.tsx",
      "parent": "/_layout"
    },
    "/_layout/collections/$collectionId/cards/$cardId": {
      "filePath": "_layout/collections/$collectionId/cards/$cardId.tsx",
      "parent": "/_layout"
    },
    "/_layout/collections/$collectionId/cards/new": {
      "filePath": "_layout/collections/$collectionId/cards/new.tsx",
      "parent": "/_layout"
    }
  }
}
ROUTE_MANIFEST_END */
